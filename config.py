import os

# بارگیری مقادیر از متغیرهای محیطی یا استفاده از مقادیر پیش‌فرض
API_ID = os.getenv("API_ID", "your_api_id_here")
API_HASH = os.getenv("API_HASH", "your_api_hash_here")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")
SESSION_NAME = os.getenv("SESSION_NAME", "default_session_name")
