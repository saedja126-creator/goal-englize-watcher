import asyncio
import aiohttp
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import os

API_ID = int(os.environ['TELEGRAM_API_ID'])
API_HASH = os.environ['TELEGRAM_API_HASH']
N8N_WEBHOOK = os.environ['N8N_WEBHOOK_URL']
SESSION_NAME = 'goal_englize_watcher'

CHANNELS = [
    '-1001844702414',  # اخبار الكرة العالمية
    '-1001681413905',  # مانشستر يونايتد بالعربي
    '-1001875447623',  # اخبار الدوري الانجليزي
]

last_seen = {ch: 0 for ch in CHANNELS}

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def poll_channels():
    async with aiohttp.ClientSession() as session:
        for channel_id in CHANNELS:
            try:
                entity = await client.get_entity(int(channel_id))
                history = await client(GetHistoryRequest(
                    peer=entity,
                    limit=5,
                    offset_date=None,
                    offset_id=0,
                    max_id=0,
                    min_id=last_seen[channel_id],
                    add_offset=0,
                    hash=0
                ))

                for message in reversed(history.messages):
                    if message.id <= last_seen[channel_id]:
                        continue
                    if not message.text:
                        continue

                    payload = {
                        'channel_id': channel_id,
                        'channel_name': entity.title,
                        'message_id': message.id,
                        'text': message.text,
                        'timestamp': message.date.isoformat(),
                        'views': getattr(message, 'views', 0)
                    }

                    async with session.post(N8N_WEBHOOK, json=payload) as resp:
                        print(f"Sent msg {message.id} from {entity.title} — status {resp.status}")

                    last_seen[channel_id] = message.id

            except Exception as e:
                print(f"Error on channel {channel_id}: {e}")

async def main():
    await client.start()
    print("Goal Englize Watcher running...")
    while True:
        await poll_channels()
        await asyncio.sleep(300)  # Every 5 minutes

asyncio.run(main())
