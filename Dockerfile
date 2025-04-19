# استفاده از پایتون 3.9
FROM python:3.9-slim

# تنظیمات برای نصب پکیج‌ها
WORKDIR /app

# کپی کردن فایل‌ها به داکر
COPY . /app

# نصب پکیج‌های مورد نیاز
RUN pip install --no-cache-dir -r requirements.txt

# دستور برای اجرای برنامه
CMD ["python", "main.py"]
