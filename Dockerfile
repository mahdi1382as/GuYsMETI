# انتخاب تصویر پایه
FROM python:3.9-slim

# تنظیمات پوشه کاری
WORKDIR /app

# نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y ffmpeg

# نصب پکیج‌های Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن تمام فایل‌ها به داخل داکر
COPY . .

# اجرای فایل main.py
CMD ["python", "main.py"]
