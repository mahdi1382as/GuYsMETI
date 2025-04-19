import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

menu = ReplyKeyboardMarkup(
    [["/start", "/help"]],
    resize_keyboard=True
)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("سلام! من آنلاینم.", reply_markup=menu)

@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    await message.reply("دستور خاصی نداری فعلاً.")

async def main():
    await app.start()
    print("Bot started.")
    await idle()
    await app.stop()

if __name__ == "__main__":
    from pyrogram.idle import idle
    asyncio.run(main())
