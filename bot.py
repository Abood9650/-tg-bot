import os, json, asyncio, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient, events, Button

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self,*a): pass

threading.Thread(target=lambda: HTTPServer(('0.0.0.0', int(os.environ.get('PORT',10000))), H).serve_forever(), daemon=True).start()

api_id   = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
token    = os.environ['BOT_TOKEN']
SOURCE   = '8838049100'

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
