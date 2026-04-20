import os
import logging
import asyncio
import base64
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

# 1. Background Server to keep Render happy
app = Flask('')
@app.route('/')
def home(): return "AuraVisual AI is Online"
def run_health_check(): app.run(host='0.0.0.0', port=10000)

# 2. Configuration
TOKEN = os.environ.get("TELEGRAM_TOKEN")
STABILITY_KEY = os.environ.get("STABILITY_KEY")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 3. AI Image Generation Logic
async def generate_image(prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {"Accept": "application/json", "Authorization": f"Bearer {STABILITY_KEY}"}
    body = {"text_prompts": [{"text": prompt}], "cfg_scale": 7, "height": 1024, "width": 1024, "samples": 1, "steps": 30}
    
    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200: return None
    
    data = response.json()
    image_data = base64.b64decode(data["artifacts"][0]["base64"])
    return image_data

# 4. Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🎨 Generate Image", callback_data='gen')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<b>Welcome to AuraVisual AI</b>\n\nSend me a text prompt, and I will generate a high-fidelity visual for you instantly.",
        parse_mode='HTML', reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    status_msg = await update.message.reply_text("⏳ Generating your visual... please wait.")
    
    try:
        image_bytes = await generate_image(prompt)
        if image_bytes:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_bytes, caption=f"✨ Generated: {prompt}")
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Sorry, something went wrong with the AI engine.")
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")

# 5. Main Execution
if __name__ == '__main__':
    Thread(target=run_health_check).start() # Starts the health check
    app_tg = ApplicationBuilder().token(TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app_tg.run_polling()
