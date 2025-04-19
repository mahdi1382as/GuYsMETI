import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from yt_dlp import YoutubeDL
from config import API_ID, API_HASH, BOT_TOKEN

bot = Client("ytbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.private & filters.text)
async def youtube_handler(client, message):
    url = message.text.strip()
    if "youtube.com" not in url and "youtu.be" not in url:
        return await message.reply("لطفاً لینک یوتیوب بده.")

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("دانلود MP3", callback_data=f"mp3|{url}"),
            InlineKeyboardButton("دانلود MP4", callback_data=f"mp4|{url}")
        ]
    ])
    await message.reply("می‌خوای به چه فرمتی دانلود کنم؟", reply_markup=keyboard)

@bot.on_callback_query()
async def button_handler(client, callback_query):
    await callback_query.answer()
    data = callback_query.data
    format_type, url = data.split("|")

    if format_type == "mp3":
        opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    else:
        opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': 'downloads/%(title)s.%(ext)s'
        }

    await callback_query.message.reply("در حال دانلود...")

    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        if format_type == "mp3":
            file_path = file_path.rsplit(".", 1)[0] + ".mp3"

    await callback_query.message.reply_document(file_path)
    os.remove(file_path)

bot.run()
