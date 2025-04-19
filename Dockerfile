FROM python:3.9-slim

# نصب پکیج‌های مورد نیاز
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . /app

WORKDIR /app
CMD ["python", "main.py"]
