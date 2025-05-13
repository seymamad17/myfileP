from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎧 جستجوی آهنگ", callback_data='search_song')],
        [InlineKeyboardButton("🔍 جستجوی متن ترانه", callback_data='search_lyrics')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! چی میخوای جستجو کنی؟", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'search_song':
        await query.edit_message_text("اسم آهنگ رو بفرست 🌐")
        context.user_data['mode'] = 'song'
    elif query.data == 'search_lyrics':
        await query.edit_message_text("بخشی از متن ترانه رو بفرست 🎤")
        context.user_data['mode'] = 'lyrics'

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('mode')
    text = update.message.text
    if mode == 'song':
        # اینجا باید API صدا یا لینک پیدا کنی
        await update.message.reply_text(f"در حال جستجوی آهنگ: {text}...")
    elif mode == 'lyrics':
        # اینجا از API مثل lyrics.ovh استفاده می‌کنیم
        await update.message.reply_text(f"در حال جستجوی متن ترانه برای: {text}...")

def main():
    app = Application.builder().token("7707789333:AAE_50ihmybcFPRbkhRvaNBEHlsufZfXOs8").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
