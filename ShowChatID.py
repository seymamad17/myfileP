from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# توکن ربات تلگرام
TOKEN = '7893837582:AAFZhB-kL5G-wANNu4e8trgYf4wti6drTnk'

# تابع برای دریافت آیدی کاربر و ارسال پیام
async def send_link(update: Update, context):
    # دریافت آیدی عددی کاربر
    user_id = update.message.text.split(' ')[1]
    
    # ارسال لینک یا پیامی برای کاربر
    message = f"این لینک برای ارسال پیام به کاربر با آیدی {user_id} است."
    await update.message.reply_text(message)

# تابع برای ارسال پیام به کاربر خاص
async def send_message_to_user(update: Update, context):
    user_id = context.args[0]  # دریافت آیدی از ورودی
    message = "پیام شما اینجا است."  # پیام دلخواه
    await context.bot.send_message(chat_id=user_id, text=message)

def main():
    application = Application.builder().token(TOKEN).build()

    # هندلرهای لازم برای دستورات
    application.add_handler(CommandHandler('sendlink', send_link))
    application.add_handler(CommandHandler('sendmessage', send_message_to_user))

    # اجرای ربات
    application.run_polling()

if __name__ == '__main__':
    main()
