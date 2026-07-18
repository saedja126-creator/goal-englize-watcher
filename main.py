"""
Goal Englize Telegram Watcher - v2 (photo capture)

WHAT CHANGED FROM v1
  v1 had `if not text: continue` and never touched media, so every image these
  channels publish was thrown away. 87% of their posts carry a photo, and Saed's
  whole pipeline depends on it (good photo -> free fact card, weak photo -> AI
  reference). v2 downloads the photo and ships it with the text.

HOW THE PHOTO TRAVELS
  Base64 inside the same JSON webhook. Measured on 60 real samples these photos
  run 41-400 KB (typ. ~150 KB), so base64 adds ~33% and the payload stays small.
  No extra storage, no public URLs, no second service to keep alive.

  Photos are NOT forwarded to Saed's Telegram here - that would spam him with
  every junk post before scoring. n8n scores first and only surfaces winners.

ENV
  TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION_STRING, N8N_WEBHOOK_URL
  DRY_RUN=1        - print what would be sent, send nothing (local testing)
  BACKFILL=N       - on boot, replay the last N messages per channel, then poll
  MAX_PHOTO_MB     - skip photos larger than this (default 4)
"""

import asyncio
import base64
import io
import os
import sys

try:
    import aiohttp
except ImportError:          # only needed to actually POST; DRY_RUN works without it
    aiohttp = None
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetHistoryRequest

# Windows consoles are cp1252 and crash on Arabic channel titles.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _load_local_env():
    """Local testing convenience. On Railway the real env vars win."""
    path = r"E:\Saed-Workspace\01_GoalEnglize\00_START-HERE\watcher_creds.env"
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


_load_local_env()

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
SESSION_STRING = os.environ["TELEGRAM_SESSION_STRING"]
N8N_WEBHOOK = os.environ.get("N8N_WEBHOOK_URL", "")

DRY_RUN = os.environ.get("DRY_RUN") == "1"
BACKFILL = int(os.environ.get("BACKFILL", "0"))
MAX_PHOTO_BYTES = int(float(os.environ.get("MAX_PHOTO_MB", "4")) * 1024 * 1024)

CHANNELS = ["-1001844702414", "-1001681413905", "-1001875447623"]

last_seen = {ch: 0 for ch in CHANNELS}
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


class _NullSession:
    """Stand-in used in DRY_RUN so local testing needs no aiohttp install."""
    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


def http_session():
    if DRY_RUN or aiohttp is None:
        return _NullSession()
    return aiohttp.ClientSession()


def photo_dimensions(message):
    """Largest available size of the attached photo, else (0, 0)."""
    best_w = best_h = 0
    photo = getattr(message, "photo", None)
    for size in (getattr(photo, "sizes", None) or []):
        w = getattr(size, "w", 0) or 0
        h = getattr(size, "h", 0) or 0
        if w * h > best_w * best_h:
            best_w, best_h = w, h
    return best_w, best_h


async def grab_photo(message):
    """Download the photo to memory and base64 it. Returns a dict or None.

    Never raises - a photo problem must not cost us the news item, since the
    text alone is still worth scoring.
    """
    if getattr(message, "photo", None) is None:
        return None
    try:
        buf = io.BytesIO()
        await client.download_media(message, file=buf)
        raw = buf.getvalue()
        if not raw:
            return None
        if len(raw) > MAX_PHOTO_BYTES:
            print("  [PHOTO SKIPPED] %d bytes over limit" % len(raw))
            return None
        w, h = photo_dimensions(message)
        return {
            "b64": base64.b64encode(raw).decode("ascii"),
            "bytes": len(raw),
            "width": w,
            "height": h,
            "ratio": round(w / h, 3) if h else None,
        }
    except Exception as exc:
        print("  [PHOTO ERROR] msg %s: %s" % (getattr(message, "id", "?"), exc))
        return None


async def send_to_n8n(session, payload, message_id, title):
    if DRY_RUN:
        p = payload["body"]
        ph = p.get("photo")
        print("  [DRY RUN] msg %s | text %d chars | photo %s" % (
            message_id, len(p.get("text") or ""),
            ("%dx%d %dKB" % (ph["width"], ph["height"], ph["bytes"] // 1024)) if ph else "none"))
        return
    try:
        async with session.post(N8N_WEBHOOK, json=payload,
                                timeout=aiohttp.ClientTimeout(total=30)) as resp:
            print("  [SENT] msg %s from %s -> HTTP %s" % (message_id, title, resp.status))
    except Exception as exc:
        print("  [SEND ERROR] msg %s: %s" % (message_id, exc))


async def handle_message(session, message, channel_id, title):
    text = getattr(message, "text", None) or getattr(message, "message", None)
    if not text or not text.strip():
        # Photo-only posts carry nothing to rephrase, so they are not news items.
        return False

    photo = await grab_photo(message)

    payload = {"body": {
        "channel_id": channel_id,
        "channel_name": title,
        "message_id": message.id,
        "text": text,
        "timestamp": message.date.isoformat(),
        "views": getattr(message, "views", 0),
        "has_photo": photo is not None,
        "photo": photo,
    }}
    await send_to_n8n(session, payload, message.id, title)
    return True


async def poll_channels():
    try:
        if not client.is_connected():
            print("[RECONNECT] Reconnecting...")
            await asyncio.wait_for(client.connect(), timeout=15)
    except Exception as exc:
        print("[RECONNECT FAILED] %s - skipping cycle" % exc)
        return

    print("[POLL] Checking channels...")
    async with http_session() as session:
        for channel_id in CHANNELS:
            try:
                entity = await client.get_entity(int(channel_id))
                history = await client(GetHistoryRequest(
                    peer=entity, limit=20, offset_date=None, offset_id=0,
                    max_id=0, min_id=0, add_offset=0, hash=0))
                new_msgs = [m for m in history.messages if m.id > last_seen[channel_id]]
                if new_msgs:
                    print("[%s] %d new" % (entity.title, len(new_msgs)))
                for message in reversed(new_msgs):
                    await handle_message(session, message, channel_id, entity.title)
                    last_seen[channel_id] = message.id
            except Exception as exc:
                print("[CHANNEL ERROR] %s: %s" % (channel_id, exc))


async def run_backfill(n):
    """Replay the last N messages per channel once, so the pipeline has real
    material to work with immediately instead of waiting for live news."""
    print("[BACKFILL] replaying last %d per channel..." % n)
    async with http_session() as session:
        for channel_id in CHANNELS:
            try:
                entity = await client.get_entity(int(channel_id))
                sent = 0
                async for message in client.iter_messages(entity, limit=n):
                    if await handle_message(session, message, channel_id, entity.title):
                        sent += 1
                print("[BACKFILL] %s -> %d sent" % (entity.title, sent))
            except Exception as exc:
                print("[BACKFILL ERROR] %s: %s" % (channel_id, exc))


async def main():
    await client.connect()
    if not await client.is_user_authorized():
        sys.exit("Session string is not authorised.")
    print("Goal Englize Watcher v2 (photo capture)%s" % ("  [DRY RUN]" if DRY_RUN else ""))

    for channel_id in CHANNELS:
        try:
            entity = await client.get_entity(int(channel_id))
            history = await client(GetHistoryRequest(
                peer=entity, limit=1, offset_date=None, offset_id=0,
                max_id=0, min_id=0, add_offset=0, hash=0))
            if history.messages:
                last_seen[channel_id] = history.messages[0].id
                print("[INIT] %s from msg %s" % (entity.title, last_seen[channel_id]))
        except Exception as exc:
            print("[INIT ERROR] %s: %s" % (channel_id, exc))

    if BACKFILL:
        await run_backfill(BACKFILL)

    print("[READY] Polling every 60s...")
    while True:
        try:
            await poll_channels()
        except Exception as exc:
            print("[LOOP ERROR] %s - retrying in 30s" % exc)
            await asyncio.sleep(30)
            continue
        await asyncio.sleep(60)


asyncio.run(main())
