import re
from telethon.sync import TelegramClient, events


api_id = 21035788
api_hash = 'f3bbc8876a1305569eaab57bdde12811'
target_group_id = -1001991083116

with open('chats.csv', 'r', encoding='utf-8') as chats_file, \
     open('keywords.csv', 'r', encoding='utf-8') as keywords_file, \
     open('keywords_minus.csv', 'r', encoding='utf-8') as minus_file:
     chat_links = [line.strip() for line in chats_file]
     keywords = [line.strip() for line in keywords_file]
     keywords_minus = [line.strip() for line in minus_file]

with TelegramClient('tele2_handler', api_id, api_hash) as client:
    target_chats = []

    for link in chat_links:
        entity = client.get_entity(link)
        if entity:
            target_chats.append(entity.id)


    @client.on(events.NewMessage(chats=target_chats))
    async def handle_new_message(event):
        message_text = event.message.text
        message_link = f'https://t.me/{event.chat.username}/{event.message.id}'
        forward_data = f'{message_link}\n\n{message_text}'

        if any(re.search(fr'\b{re.escape(keyword)}\b', message_text, re.IGNORECASE) for keyword in keywords):
            await client.send_message(target_group_id, forward_data)
            print(f'Message found: {message_link}')


    client.run_until_disconnected()
