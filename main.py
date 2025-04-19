import os
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from pathlib import Path

# تنظیمات
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("kirvakosdalag", api_id=487410, api_hash="6d96f6d419ad8bc4a5181745d9228331", bot_token="773349916:AAEhxMKH2yOH6oqu5OPLZ-M2LM9qnwvzFFI")

# منوی اصلی
def start_markup():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("MP3", callback_data="mp3"),
             InlineKeyboardButton("MP4", callback_data="mp4")]
        ]
    )

# منوی انتخاب کیفیت
def quality_markup(is_mp4=False):
    if is_mp4:
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("240p", callback_data="240p"),
                 InlineKeyboardButton("480p", callback_data="480p"),
                 InlineKeyboardButton("720p", callback_data="720p"),
                 InlineKeyboardButton("1080p", callback_data="1080p"),
                 InlineKeyboardButton("4K", callback_data="4K"),
                 InlineKeyboardButton("60fps", callback_data="60fps"),
                 InlineKeyboardButton("90fps", callback_data="90fps"),
                 InlineKeyboardButton("120fps", callback_data="120fps")]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("128kbps", callback_data="128"),
                 InlineKeyboardButton("320kbps", callback_data="320")]
            ]
        )

# دانلود MP3 یا MP4
async def download_video(url, quality="320kbps", fps=None):
    ydl_opts = {
        'format': 'bestaudio/best' if 'mp3' in quality else f'bestvideo[height={quality}]+bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }

    # اگر فریم ریت وجود داشت
    if fps:
        ydl_opts['format'] = f'bestvideo[height={quality}][fps={fps}]+bestaudio/best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_url = info_dict['url']
    return video_url

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("سلام! لینک یوتیوب خود را ارسال کنید.",
                         reply_markup=start_markup())

@app.on_callback_query(filters.regex('^(mp3|mp4)$'))
async def quality_selection(client, callback_query):
    data = callback_query.data
    await callback_query.answer()
    if data == "mp3":
        await callback_query.message.edit("انتخاب کیفیت MP3:", reply_markup=quality_markup())
    elif data == "mp4":
        await callback_query.message.edit("انتخاب کیفیت MP4:", reply_markup=quality_markup(is_mp4=True))

@app.on_callback_query(filters.regex('^(128|320|240p|480p|720p|1080p|4K|60fps|90fps|120fps)$'))
async def download(client, callback_query):
    data = callback_query.data
    await callback_query.answer()

    # تشخیص کیفیت انتخابی
    if 'p' in data or 'K' in data:
        quality = data
        file_type = "mp4"
    else:
        quality = f"{data}kbps"
        file_type = "mp3"

    fps = None
    if 'fps' in data:
        fps = data

    url = callback_query.message.reply_to_message.text
    await callback_query.message.edit("در حال دانلود فایل...")

    # دانلود فایل
    video_url = await download_video(url, quality, fps)
    
    await callback_query.message.reply("فایل دانلود شد.", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("دانلود", url=video_url)]
    ]))

    # حذف فایل از سرور بعد از ارسال
    file_path = Path(f"downloads/{url.split('=')[-1]}.{file_type}")
    if file_path.exists():
        os.remove(file_path)
