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
SOURCE   = int(os.environ['CHANNEL_ID'])

ids = json.load(open('msgs.json'))
bot = TelegramClient('srv', api_id, api_hash).start(bot_token=token)

@bot.on(events.NewMessage(pattern='/start'))
async def start(e):
    await e.respond(f'أهلاً 👋\n\nعندي {len(ids)} ملف.',
        buttons=[[Button.inline('🎬 كل الملفات', b'all')]])

@bot.on(events.CallbackQuery)
async def press(e):
    await e.respond(f'إرسال {len(ids)} ملف...')
    ok=0
    for i in range(0, len(ids), 20):
        try:
            await bot.forward_messages(e.chat_id, ids[i:i+20], SOURCE)
            ok += len(ids[i:i+20])
        except Exception as ex: print(ex)
        await asyncio.sleep(2)
    await e.respond(f'✅ تم — {ok}')

print('شغال')
bot.run_until_disconnected()
