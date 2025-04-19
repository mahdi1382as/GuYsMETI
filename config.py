import os

# متغیرهای API و TOKEN از Railway یا محیط‌های دیگر (یا به صورت دستی)
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# اگر نیاز به یک session name دارید، باید این متغیر را تعریف کنید
SESSION_NAME = os.getenv("SESSION_NAME", "default_session_name")
