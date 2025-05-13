# استفاده از یک تصویر پایه (base image)
FROM python:3.9-slim

# نصب وابستگی‌های سیستم (مثل ffmpeg)
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 && rm -rf /var/lib/apt/lists/*

# تعیین دایرکتوری کاری داخل کانتینر
WORKDIR /app

# کپی کردن فایل‌های پروژه به داخل کانتینر
COPY . /app/

# ساخت محیط مجازی
RUN python -m venv /opt/venv

# فعال کردن محیط مجازی و نصب پکیج‌ها
RUN /opt/venv/bin/pip install -r /app/requirements.txt --no-cache-dir --verbose

# تنظیم مسیر محیط مجازی
ENV PATH="/opt/venv/bin:$PATH"

# اجرای ربات
CMD ["python", "bot.py"]
