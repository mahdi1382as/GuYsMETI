import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from yt_dlp import YoutubeDL
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# دکمه‌ها
control_buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("▶️ پخش", callback_data="play")],
    [InlineKeyboardButton("⏹ توقف", callback_data="stop")]
])

main_menu = ReplyKeyboardMarkup([
    ["/start", "/help"],
    ["/play لینک"]
], resize_keyboard=True)

# دانلود لینک صوتی از یوتیوب
def yt_download(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'extract_flat': False,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url'], info.get('title', 'Unknown')

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply(
        "سلام! لینک یوتیوب رو بفرست تا صدای اون رو بفرستم.",
        reply_markup=main_menu
    )

@app.on_message(filters.command("play"))
async def play(client, message: Message):
    if len(message.command) < 2:
        await message.reply("لطفاً یک لینک یوتیوب وارد کن.")
        return
    url = message.command[1]
    try:
        audio_url, title = yt_download(url)
        await message.reply_audio(
            audio_url,
            caption=f"🎵 {title}",
            reply_markup=control_buttons
        )
    except Exception as e:
        await message.reply(f"خطا در پردازش لینک: {e}")

@app.on_callback_query()
async def handle_buttons(client, callback_query):
    data = callback_query.data
    if data == "play":
        await callback_query.answer("در حال پخش فایل صوتی!")
    elif data == "stop":
        await callback_query.answer("پخش متوقف شد.")

async def main():
    await app.start()
    print("ربات اجرا شد.")
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
