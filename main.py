import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, InputAudioStream
from pytgcalls.types.stream import StreamType
from yt_dlp import YoutubeDL
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("bot", api_id=487410, api_hash="6d96f6d419ad8bc4a5181745d9228331", bot_token="773349916:AAEhxMKH2yOH6oqu5OPLZ-M2LM9qnwvzFFI")
pytg = PyTgCalls(app)

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(title)s.%(ext)s",
}

@app.on_message(filters.audio & filters.group)
async def handle_audio(client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("پخش در ویس‌چت", callback_data=f"play|{message.chat.id}|{message.audio.file_id}")]]
    )
    await message.reply_text("می‌خوای این آهنگ رو پخش کنم؟", reply_markup=keyboard)

@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data.split("|")
    if data[0] == "play":
        chat_id = int(data[1])
        file_id = data[2]
        file_path = await app.download_media(file_id)
        await pytg.join_group_call(
            chat_id,
            InputStream(InputAudioStream(file_path)),
            stream_type=StreamType().local_stream,
        )
        await callback_query.answer("در حال پخش در ویس‌چت!", show_alert=True)

async def main():
    await app.start()
    await pytg.start()
    print("ربات با موفقیت اجرا شد.")
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
