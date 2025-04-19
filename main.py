import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from yt_dlp import YoutubeDL
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME

# ساخت کلاینت‌ها
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(userbot)

# صف‌ها
queues = {}

# استخراج لینک صوتی از یوتیوب
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

# دکمه‌های شیشه‌ای کنترل پخش
control_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("⏸ Pause", callback_data="pause"),
        InlineKeyboardButton("⏭ Skip", callback_data="skip"),
    ],
    [
        InlineKeyboardButton("⏹ Stop", callback_data="stop")
    ]
])

# منوی پاسخگو
main_menu = ReplyKeyboardMarkup(
    [["/play", "/pause"], ["/skip", "/stop"]],
    resize_keyboard=True
)

# فرمان شروع
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply(
        "سلام! من یک بات پخش موزیک هستم. از دکمه‌های زیر استفاده کن:",
        reply_markup=main_menu
    )

# فرمان پخش موزیک
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

# اتصال به ویس چت و پخش
async def join_and_play(chat_id, audio_url):
    await pytgcalls.join_group_call(
        chat_id,
        InputStream(
            InputAudioStream(audio_url)
        ),
        stream_type="local"
    )

# کنترل از طریق دکمه‌های شیشه‌ای
@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data == "pause":
        await pytgcalls.pause_stream(chat_id)
        await callback_query.answer("⏸ پخش متوقف شد")
    elif data == "skip":
        if chat_id in queues and len(queues[chat_id]) > 1:
            queues[chat_id].pop(0)
            next_audio, title = queues[chat_id][0]
            await join_and_play(chat_id, next_audio)
            await callback_query.answer(f"⏭ در حال پخش: {title}")
        else:
            await callback_query.answer("صف پخش خالی است")
    elif data == "stop":
        await pytgcalls.leave_group_call(chat_id)
        queues[chat_id] = []
        await callback_query.answer("⏹ پخش متوقف شد")

# فرمان توقف دستی
@app.on_message(filters.command("pause") & filters.group)
async def pause(_, message: Message):
    await pytgcalls.pause_stream(message.chat.id)
    await message.reply("⏸ پخش متوقف شد")

# فرمان رفتن به موزیک بعدی
@app.on_message(filters.command("skip") & filters.group)
async def skip(_, message: Message):
    chat_id = message.chat.id
    if chat_id in queues and len(queues[chat_id]) > 1:
        queues[chat_id].pop(0)
        next_audio, title = queues[chat_id][0]
        await join_and_play(chat_id, next_audio)
        await message.reply(f"⏭ در حال پخش: {title}")
    else:
        await message.reply("صف پخش خالی است")

# فرمان توقف کامل
@app.on_message(filters.command("stop") & filters.group)
async def stop(_, message: Message):
    chat_id = message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    queues[chat_id] = []
    await message.reply("⏹ پخش متوقف شد")

# ادامه پخش
@app.on_message(filters.command("resume") & filters.group)
async def resume(_, message: Message):
    await pytgcalls.resume_stream(message.chat.id)
    await message.reply("▶️ ادامه پخش")

# اجرای اصلی برنامه
async def main():
    await app.start()
    await userbot.start()
    await pytgcalls.start()
    print("ربات آماده است")
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
