import discord
import random
import os
import http.server
import socketserver
from threading import Thread
# --- ĐOẠN CODE MỞ CỔNG GIẢ CHO RENDER ---
def keep_alive():
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running!")

    def run_server():
        # Render mặc định dùng cổng 10000 hoặc bạn có thể lấy từ biến môi trường
        port = int(os.environ.get("PORT", 10000))
        with socketserver.TCPServer(("0.0.0.0", port), Handler) as httpd:
            httpd.serve_forever()

    Thread(target=run_server, daemon=True).start()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN chưa được set trong environment variables")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

messages = [
    "Hú hú, khẹc khẹc, ẳng ẳng, meo meo, gâu gâu, húuuuuuuuu, áuuuuuuuu",
    "Ngậm miệng lại, đi ra cửa, đến chợ mua 1 con cá, bắt chuyến xe ra sân bay, bay đến NASA, đăng kí 1 suất tình nguyện viên khám phá hành tinh mới, leo lên tên lửa, đến vùng đất mới và dựng lều trại, nướng con cá, ăn no và ở lại đó. Ngay và luôn",
    "Gọi hoài, biết tui đẹp nhất server rồi 😎",
    "Câm ngay cho chụy, em phải xóa acc và gửi chị 100 củ để chụy không kêu công an còng đầu em ra Côn Đảo. Chị nhắc lại, em xóa acc ngay và gửi 100 triệu vào tài khoản của chị ngay",
    "Ngủ đi, ngủ không ngon 😴"
]

shuffled = []
index = 0

def reset_messages():
    global shuffled, index
    shuffled = messages.copy()
    random.shuffle(shuffled)
    index = 0

reset_messages()

@client.event
async def on_ready():
    print(f'Bot online: {client.user}')

@client.event
async def on_message(message):
    global index

    if message.author == client.user:
        return

    if client.user in message.mentions:
        if index >= len(shuffled):
            reset_messages()

        await message.channel.send(shuffled[index])
        index += 1

keep_alive()
client.run(TOKEN)