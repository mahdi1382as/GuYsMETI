import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from yt_dlp import YoutubeDL
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

queues = {}

# تابع دانلود لینک از یوتیوب
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
    return info['url'], info['title']

# دکمه‌ها
control_buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("⏸ Pause", callback_data="pause"),
     InlineKeyboardButton("⏭ Skip", callback_data="skip")],
    [InlineKeyboardButton("⏹ Stop", callback_data="stop")]
])

# منوی پاسخگو
main_menu = ReplyKeyboardMarkup([["/play", "/pause"], ["/skip", "/stop"]], resize_keyboard=True)

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply("سلام! من یک بات پخش موزیک هستم. از دکمه‌های زیر استفاده کن:", reply_markup=main_menu)

@app.on_message(filters.command("play") & filters.group)
async def play(_, message: Message):
    if len(message.command) < 2:
        await message.reply("لطفاً لینک یوتیوب را وارد کنید.")
        return

    url = message.command[1]
    chat_id = message.chat.id

    if chat_id not in queues:
        queues[chat_id] = []

    audio_url, title = yt_download(url)
    queues[chat_id].append((audio_url, title))

    if len(queues[chat_id]) > 1:
        await message.reply(f"'{title}' به صف پخش اضافه شد.", reply_markup=main_menu)
        return

    await join_and_play(chat_id, audio_url)
    await message.reply(f"در حال پخش: {title}", reply_markup=control_buttons)

async def join_and_play(chat_id, audio_url):
    # در اینجا باید کدی برای پخش موزیک بنویسید
    pass

@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data == "pause":
        # پخش متوقف می‌شود
        pass
    elif data == "skip":
        # موزیک بعدی پخش می‌شود
        pass
    elif data == "stop":
        # پخش متوقف می‌شود
        pass

@app.on_message(filters.command("pause") & filters.group)
async def pause(_, message: Message):
    # پخش متوقف می‌شود
    pass

@app.on_message(filters.command("skip") & filters.group)
async def skip(_, message: Message):
    # موزیک بعدی پخش می‌شود
    pass

@app.on_message(filters.command("stop") & filters.group)
async def stop(_, message: Message):
    # پخش متوقف می‌شود
    pass

async def main():
    await app.start()
    await userbot.start()
    print("ربات آماده است")

    # استفاده از `get_event_loop` برای جلوگیری از ایجاد `event loop` جدید
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    # از `run_until_complete` برای اجرای تابع `main()` استفاده نمی‌کنیم
    # چون در محیط‌هایی که قبلاً `event loop` اجرا شده این خطا پیش میاد
    asyncio.get_event_loop().run_until_complete(main())
