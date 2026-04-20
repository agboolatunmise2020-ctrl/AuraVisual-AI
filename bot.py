import os
import logging
import base64
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# 1. Setup & Config
TOKEN = os.environ.get("TELEGRAM_TOKEN")
STABILITY_KEY = os.environ.get("STABILITY_KEY")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎨 Generate New Image", callback_data='help_prompt')],
        [
            InlineKeyboardButton("📜 Examples", callback_data='examples'),
            InlineKeyboardButton("⚙️ Settings", callback_data='settings')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<b>Welcome to AuraVisual AI</b>\n\nSend a text prompt to create a visual!",
        parse_mode='HTML', reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'help_prompt':
        await query.message.reply_text("Just send me a description of the image you want!")
    elif query.data == 'examples':
        await query.message.reply_text("Try: 'A futuristic city' or 'A cute robot drinking coffee'.")
    elif query.data == 'settings':
        await query.message.reply_text("Settings: Resolution 1024x1024 is active.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # (Your existing image generation logic goes here)
    pass

# 3. The Main Block (CRITICAL FIX)
if __name__ == '__main__':
    app_tg = ApplicationBuilder().token(TOKEN).build()
    
    # Registering all handlers
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(CallbackQueryHandler(button_callback)) # <--- MUST HAVE THIS
    app_tg.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    logger.info("AuraVisual AI is starting...")
    app_tg.run_polling(drop_pending_updates=True)
