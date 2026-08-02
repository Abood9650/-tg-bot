import os, asyncio, threading
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

bot = TelegramClient('srv', api_id, api_hash).start(bot_token=token)

@bot.on(events.NewMessage(pattern='/start'))
async def start(e):
    await e.respond('أهلاً 👋\n\nاختر:',
        buttons=[[Button.inline('🎬 كل الملفات', b'all')]])

@bot.on(events.CallbackQuery)
async def press(e):
    await e.respond('جاري الإرسال...')
    ok=0
    async for m in bot.iter_messages(SOURCE, reverse=True):
        if m.document:
            try:
                await bot.forward_messages(e.chat_id, m)
                ok+=1
                if ok%20==0: await asyncio.sleep(2)
            except Exception as ex: print(ex)
    await e.respond(f'✅ تم — {ok}')

print('شغال')
bot.run_until_disconnected()
