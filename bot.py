import os, json, asyncio
from telethon import TelegramClient, events, Button

api_id   = int(os.environ['30523401'])
api_hash = os.environ['50bb2db1976e4bcbacc14b32d8287b82']
token    = os.environ['8537132771:AAEMa0YGQMBz_26Xbw4fOpt3X50SAIp3rW8']
SOURCE   = 'K07Bbot'

items = json.load(open('files.json'))
bot = TelegramClient('srv', api_id, api_hash).start(bot_token=token)

@bot.on(events.NewMessage(pattern='/start'))
async def start(e):
    await e.respond(f'أهلاً 👋\n\nعندي {len(items)} ملف.',
        buttons=[[Button.inline('🎬 كل الملفات', b'all')],
                 [Button.inline('📊 الأصغر أولاً', b'small')]])

@bot.on(events.CallbackQuery)
async def press(e):
    lst = sorted(items, key=lambda x:x['size']) if e.data==b'small' else items
    await e.respond(f'إرسال {len(lst)} ملف...')
    for i,it in enumerate(lst,1):
        try:
            m = await bot.get_messages(SOURCE, ids=it['id'])
            await bot.send_file(e.chat_id, m.document, caption=it['caption'])
        except Exception as ex: print(ex)
        if i%20==0: await asyncio.sleep(2)
    await e.respond('✅ تم')

print('شغال')
bot.run_until_disconnected()
