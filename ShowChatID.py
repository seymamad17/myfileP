import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest
from telegram.error import TelegramError

# توکن ربات و آیدی عددی ادمین
TOKEN = "7893837582:AAFZhB-kL5G-wANNu4e8trgYf4wti6drTnk"
ADMIN_ID = 7507284671

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    chat_id = update.message.chat_id
    try:
        await update.message.reply_text(
            f"سلام! آیدی چت شما: {chat_id}\n"
            "برای گرفتن لینک چت یه کاربر، از این دستور استفاده کنید:\n"
            "/getlink <chat_id>\n"
            "مثال: /getlink 123456789"
        )
    except TelegramError as e:
        print(f"خطا در ارسال پیام: {e}")
        await context.bot.send_message(chat_id=chat_id, text="خطا در ارتباط با تلگرام.")

# /getlink
async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    chat_id = update.message.chat_id

    if chat_id != ADMIN_ID:
        await update.message.reply_text("فقط ادمین می‌تونه از این دستور استفاده کنه!")
        return

    args = context.args
    if len(args) != 1:
        await update.message.reply_text("فرمت دستور نادرست است:\n/getlink <chat_id>")
        return

    try:
        target_chat_id = int(args[0])
        link = f"tg://user?id={target_chat_id}"
        await update.message.reply_text(f"🔗 لینک چت:\n{link}")
    except ValueError:
        await update.message.reply_text("آیدی باید عدد باشد.")
    except TelegramError as e:
        print(f"خطا: {e}")
        await update.message.reply_text("خطا در ارسال پیام.")

# اجرای ربات
async def main():
    print("🤖 ربات در حال اجراست...")
    try:
        request = HTTPXRequest(connection_timeout=30)
        app = Application.builder().token(TOKEN).http_request(request).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("getlink", get_link))

        await app.run_polling()
    except Exception as e:
        print(f"❌ خطا در اجرا: {e}")

if __name__ == "__main__":
    asyncio.run(main())
