import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import youtube_dl

# اطلاعات تنظیمات
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# دانلود لینک صوتی از یوتیوب
def yt_download(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'extract_flat': False,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url'], info['title']

# دکمه‌های کنترلی
control_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("⏸ Pause", callback_data="pause"),
        InlineKeyboardButton("⏭ Skip", callback_data="skip"),
    ],
    [InlineKeyboardButton("⏹ Stop", callback_data="stop")]
])

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply("سلام! من یک بات پخش موزیک هستم. از دکمه‌های زیر استفاده کن:", reply_markup=control_buttons)

@app.on_message(filters.command("play") & filters.group)
async def play(_, message: Message):
    if len(message.command) < 2:
        await message.reply("لطفاً لینک یوتیوب را وارد کنید.")
        return

    url = message.command[1]
    chat_id = message.chat.id

    audio_url, title = yt_download(url)

    # ارسال فایل صوتی به گروه
    await app.send_audio(chat_id, audio_url)
    await message.reply(f"در حال پخش: {title}", reply_markup=control_buttons)

@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data == "pause":
        await callback_query.answer("⏸ پخش متوقف شد")
    elif data == "skip":
        await callback_query.answer("⏭ موزیک بعدی در حال پخش است.")
    elif data == "stop":
        await callback_query.answer("⏹ پخش متوقف شد")

async def main():
    await app.start()
    print("ربات آماده است")
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
