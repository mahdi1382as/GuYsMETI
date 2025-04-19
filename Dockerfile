FROM python:3.10-slim

WORKDIR /app

# نصب پکیج‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . .

# اجرای فایل اصلی
CMD ["python3", "main.py"]
