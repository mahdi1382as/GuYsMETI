# استفاده از تصویر پایه پایتون
FROM python:3.9-slim

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی فایل‌ها به کانتینر
COPY . /app

# نصب پکیج‌های مورد نیاز
RUN pip install --no-cache-dir -r requirements.txt

# اجرای برنامه
CMD ["python", "main.py"]
