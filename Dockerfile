FROM python:3.9-slim

# تنظیمات برای به روزرسانی و نصب ابزارهای مورد نیاز
RUN apt-get update && apt-get install -y python3-dev build-essential

# کپی requirements.txt
COPY requirements.txt .

# نصب پکیج‌ها
RUN pip install --no-cache-dir -r requirements.txt

# کپی سایر فایل‌های پروژه
COPY . /app

WORKDIR /app

# اجرای ربات
CMD ["python", "main.py"]
