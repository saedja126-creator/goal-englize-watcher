import asyncio
import aiohttp
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import os

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
N8N_WEBHOOK = os.environ["N8N_WEBHOOK_URL"]
SESSION_NAME = "goal_englize_watcher"

CHANNELS = ["-1001844702414","-1001681413905","-1001875447623"]
last_seen = {ch: 0 for ch in CHANNELS}
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def poll_channels():
    if not client.is_connected():
        await client.connect()
    print("[POLL] Checking channels...")
    async with aiohttp.ClientSession() as session:
        for channel_id in CHANNELS:
            try:
                entity = await client.get_entity(int(channel_id))
                history = await client(GetHistoryRequest(
                    peer=entity, limit=20, offset_date=None,
                    offset_id=0, max_id=0, min_id=0,
                    add_offset=0, hash=0
                ))
                new_msgs = [m for m in history.messages if m.id > last_seen[channel_id]]
                text_msgs = [m for m in new_msgs if getattr(m,"text",None) or getattr(m,"message",None)]
                print(f"[{entity.title}] {len(new_msgs)} new total, {len(text_msgs)} with text (last_seen={last_seen[channel_id]}, latest={history.messages[0].id if history.messages else 0})")
                for message in reversed(new_msgs):
                    text = getattr(message,"text",None) or getattr(message,"message",None)
                    if not text:
                        last_seen[channel_id] = message.id
                        continue
                    payload = {
                        "body": {
                            "channel_id": channel_id,
                            "channel_name": entity.title,
                            "message_id": message.id,
                            "text": text,
                            "timestamp": message.date.isoformat(),
                            "views": getattr(message,"views",0)
                        }
                    }
                    async with session.post(N8N_WEBHOOK, json=payload) as resp:
                        print(f"[SENT] msg {message.id} from {entity.title} status {resp.status}")
                    last_seen[channel_id] = message.id
            except Exception as e:
                print(f"[ERROR] {channel_id}: {e}")

async def main():
    await client.connect()
    print("Goal Englize Watcher running...")
    for channel_id in CHANNELS:
        try:
            entity = await client.get_entity(int(channel_id))
            history = await client(GetHistoryRequest(
                peer=entity, limit=1, offset_date=None,
                offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0
            ))
            if history.messages:
                last_seen[channel_id] = history.messages[0].id
                print(f"[INIT] {entity.title} from msg {last_seen[channel_id]}")
        except Exception as e:
            print(f"[INIT ERROR] {channel_id}: {e}")
    print("[READY] Polling every 60s...")
    while True:
        await poll_channels()
        await asyncio.sleep(60)

asyncio.run(main())
