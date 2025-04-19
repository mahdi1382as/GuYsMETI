from pyrogram import Client, filters
import os

app = Client(
    "my_bot",
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN")
)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply("سلام! ربات فعاله.")

if __name__ == "__main__":
    print("ربات در حال اجراست...")
    app.run()
