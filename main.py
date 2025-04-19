from pyrogram import Client, filters
import config

app = Client(
    "my_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply("سلام! ربات فعاله.")

if __name__ == "__main__":
    print("ربات در حال اجراست...")
    app.run()
