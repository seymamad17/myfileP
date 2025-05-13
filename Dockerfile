# استفاده از یک تصویر پایه (base image)
FROM python:3.9-slim

# نصب وابستگی‌های سیستم (مثل ffmpeg)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# تعیین دایرکتوری کاری داخل کانتینر
WORKDIR /app

# کپی کردن فایل‌های پروژه به داخل کانتینر
COPY . /app/

# نصب پکیج‌ها از requirements.txt
RUN pip install -r requirements.txt --no-cache-dir --verbose

# تنظیم مسیر محیط مجازی برای اجرا
ENV PATH="/opt/venv/bin:$PATH"

# اجرای ربات
CMD ["python", "bot.py"]
