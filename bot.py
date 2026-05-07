import os
import logging
import io
import img2pdf
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# 1. Setup & Config
TOKEN = os.environ.get("TELEGRAM_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Store user images in memory {user_id: [list_of_image_bytes]}
user_sessions = {}

# 2. Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = [] # Reset session
    
    # Clean, compliant button layout
    keyboard = [
        [InlineKeyboardButton("📄 Generate PDF", callback_data='convert')],
        [InlineKeyboardButton("🗑️ Clear Images", callback_data='clear')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "<b>Welcome to AuraVisual PDF</b> 📄\n\n"
        "Convert your images into professional PDFs instantly.\n\n"
        "1️⃣ Send me one or more photos.\n"
        "2️⃣ Click <b>Generate PDF</b> when finished."
    )
    
    await update.message.reply_text(welcome_text, parse_mode='HTML', reply_markup=reply_markup)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    
    photo_file = await update.message.photo[-1].get_file()
    image_bytes = await photo_file.download_as_bytearray()
    user_sessions[user_id].append(bytes(image_bytes))
    
    count = len(user_sessions[user_id])
    await update.message.reply_text(f"✅ Image {count} received. Click 'Generate PDF' when ready.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'convert':
        if user_id not in user_sessions or not user_sessions[user_id]:
            await query.message.reply_text("❌ Please send photos first!")
            return

        status_msg = await query.message.reply_text("⏳ Compiling your PDF...")
        try:
            pdf_bytes = img2pdf.convert(user_sessions[user_id])
            await context.bot.send_document(
                chat_id=user_id,
                document=io.BytesIO(pdf_bytes),
                filename="AuraVisual_Export.pdf",
                caption="✨ Your PDF is ready!"
            )
            user_sessions[user_id] = [] 
            await status_msg.delete()
        except Exception as e:
            logger.error(f"PDF Error: {e}")
            await status_msg.edit_text("❌ Error creating PDF.")

    elif query.data == 'clear':
        user_sessions[user_id] = []
        await query.message.reply_text("🗑️ Session cleared.")

# 3. Main Execution
if __name__ == '__main__':
    if not TOKEN:
        logger.critical("CRITICAL: Missing TELEGRAM_TOKEN environment variable!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_callback))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        
        logger.info("AuraVisual PDF Bot is starting...")
        app.run_polling(drop_pending_updates=True)
