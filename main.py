import asyncio
import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME

# ایجاد ربات
app = Client("bot", api_id=487410, api_hash=6d96f6d419ad8bc4a5181745d9228331, bot_token=773349916:AAEhxMKH2yOH6oqu5OPLZ-M2LM9qnwvzFFI)
userbot = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

# تنظیمات دانلود آهنگ با yt-dlp
ydl_opts = {
    'format': 'bestaudio/best', 
    'postprocessors': [{
        'key': 'FFmpegAudioConvertor',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '/tmp/%(id)s.%(ext)s',
}

# پخش موزیک با لینک
async def play_music(chat_id, link):
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        url = info['formats'][0]['url']

    # ارسال آهنگ به گروه
    await app.send_audio(chat_id, url)

# دستور ربات برای ارسال آهنگ
@app.on_message(filters.command('play') & filters.group)
async def play(client, message):
    # بررسی لینک آهنگ ارسال شده
    if message.reply_to_message and message.reply_to_message.text:
        link = message.reply_to_message.text
        if 'youtube.com' in link or 'youtu.be' in link:
            await play_music(message.chat.id, link)
            await message.reply("در حال پخش موزیک...")
        else:
            await message.reply("لطفاً لینک معتبر آهنگ ارسال کنید.")

# شروع ربات
async def main():
    await app.start()
    await userbot.start()
    print("ربات آماده است!")
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
