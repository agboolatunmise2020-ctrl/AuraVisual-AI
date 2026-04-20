import os
import logging
import asyncio
import base64
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Configuration
TOKEN = os.environ.get("TELEGRAM_TOKEN")
STABILITY_KEY = os.environ.get("STABILITY_KEY")

# Set up logging to see errors in the Render "Logs" tab
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. AI Image Generation Logic
async def generate_image(prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }
    body = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30
    }
    
    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        logger.error(f"Stability API Error: {response.text}")
        return None
    
    data = response.json()
    return base64.b64decode(data["artifacts"][0]["base64"])

# 3. Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>Welcome to AuraVisual AI</b>\n\nSend me a text prompt, and I will generate a high-fidelity visual for you instantly.",
        parse_mode='HTML'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    status_msg = await update.message.reply_text("⏳ Generating your visual...")
    
    try:
        image_bytes = await generate_image(prompt)
        if image_bytes:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id, 
                photo=image_bytes, 
                caption=f"✨ Generated: {prompt}"
            )
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ AI Engine busy. Please try a different prompt.")
    except Exception as e:
        logger.error(f"Handler Error: {e}")
        await status_msg.edit_text("❌ An error occurred. Please try again.")

# 4. Main Execution (Pure Worker Mode)
if __name__ == '__main__':
    if not TOKEN or not STABILITY_KEY:
        logger.critical("Missing Environment Variables!")
    else:
        logger.info("AuraVisual AI Background Worker starting...")
        app_tg = ApplicationBuilder().token(TOKEN).build()
        app_tg.add_handler(CommandHandler("start", start))
        app_tg.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        # drop_pending_updates ensures it doesn't spam you with old messages on restart
        app_tg.run_polling(drop_pending_updates=True)
