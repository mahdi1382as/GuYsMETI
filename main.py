from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import yt_dlp

# مقادیر خود را در اینجا وارد کنید
api_id = "487410"
api_hash = "6d96f6d419ad8bc4a5181745d9228331"
bot_token = "773349916:AAEhxMKH2yOH6oqu5OPLZ-M2LM9qnwvzFFI"

# ساخت ربات
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# نمایش دکمه‌های انتخاب کیفیت
def quality_buttons(video_url):
    buttons = [
        [InlineKeyboardButton("MP3 128kbps", callback_data=f"mp3_128:{video_url}")],
        [InlineKeyboardButton("MP3 320kbps", callback_data=f"mp3_320:{video_url}")],
        [InlineKeyboardButton("MP4 240p", callback_data=f"mp4_240p:{video_url}")],
        [InlineKeyboardButton("MP4 480p", callback_data=f"mp4_480p:{video_url}")],
        [InlineKeyboardButton("MP4 720p", callback_data=f"mp4_720p:{video_url}")],
        [InlineKeyboardButton("MP4 1080p", callback_data=f"mp4_1080p:{video_url}")],
    ]
    return InlineKeyboardMarkup(buttons)

# وقتی کاربر یک لینک یوتیوب ارسال می‌کند
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("سلام! لطفاً یک لینک یوتیوب ارسال کنید.")

@app.on_message(filters.text)
async def download(client, message):
    if "youtube.com" in message.text or "youtu.be" in message.text:
        # نمایش دکمه‌های انتخاب کیفیت
        await message.reply("در حال آماده‌سازی دانلود. لطفاً کیفیت را انتخاب کنید.", reply_markup=quality_buttons(message.text))
    else:
        await message.reply("لطفاً یک لینک یوتیوب معتبر ارسال کنید.")

# وقتی کاربر یک کیفیت را انتخاب می‌کند
@app.on_callback_query()
async def handle_quality(client, callback_query):
    quality, video_url = callback_query.data.split(":")
    
    ydl_opts = {}
    
    if quality == "mp3_128":
        ydl_opts = {'format': 'bestaudio/best', 'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '128'}]}
    elif quality == "mp3_320":
        ydl_opts = {'format': 'bestaudio/best', 'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '320'}]}
    elif quality == "mp4_240p":
        ydl_opts = {'format': 'bestvideo[height<=240]+bestaudio/best'}
    elif quality == "mp4_480p":
        ydl_opts = {'format': 'bestvideo[height<=480]+bestaudio/best'}
    elif quality == "mp4_720p":
        ydl_opts = {'format': 'bestvideo[height<=720]+bestaudio/best'}
    elif quality == "mp4_1080p":
        ydl_opts = {'format': 'bestvideo[height<=1080]+bestaudio/best'}

    # دانلود و ارسال فایل
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        file_url = ydl.prepare_filename(info_dict)
        await callback_query.message.reply_document(file_url)

# شروع ربات
app.run()
