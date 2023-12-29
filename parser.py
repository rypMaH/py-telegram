import time
import re
import asyncio
from datetime import datetime, timedelta
from telethon.sync import TelegramClient


api_id = 21035788
api_hash = 'f3bbc8876a1305569eaab57bdde12811'
client = TelegramClient('tele2_parser', api_id, api_hash)
group_id = -1001991083116
date_period = datetime.now() - timedelta(days=1)

start_time = time.time()

with open('chats.csv', 'r', encoding='utf-8') as chats_file,\
     open('keywords.csv', 'r', encoding='utf-8') as keywords_file,\
     open('keywords_minus.csv', 'r', encoding='utf-8') as minus_file:

     chat_links = [line.strip() for line in chats_file]
     keywords = [line.strip() for line in keywords_file]
     keywords_minus = [line.strip() for line in minus_file]

async def search_messages(chat_links, keywords, keywords_minus):
    await client.start()

    for chat_link in chat_links:
        entity = await client.get_entity(chat_link)

        matching_messages = [message for message in await client.get_messages(entity, limit=1000)
                             if message.date.replace(tzinfo=None) > date_period
                             and message.text is not None and any(re.search(fr'\b{re.escape(keyword)}\b', message.text, re.IGNORECASE) for keyword in keywords)
                             and not any(re.search(fr'\b{re.escape(keyword)}\b', message.text, re.IGNORECASE) for keyword in keywords_minus)]

        for message in matching_messages:
            message_link = f'{chat_link}/{message.id}'
            print(f'Message found: {message_link}')

            forward_data = f'Link: {message_link}\n\nText: {message.text}'
            await client.send_message(group_id, forward_data)

        await asyncio.sleep(1)

    await client.disconnect()

with client:
    client.loop.run_until_complete(search_messages(chat_links, keywords, keywords_minus))

end_time = time.time()
elapsed_time = round((end_time - start_time)/60, 1)
print("Execution time:", elapsed_time, "minutes")
