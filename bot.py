async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Professional Button Layout
    keyboard = [
        [InlineKeyboardButton("🎨 Generate New Image", callback_data='help_prompt')],
        [
            InlineKeyboardButton("📜 Examples", callback_data='examples'),
            InlineKeyboardButton("⚙️ Settings", callback_data='settings')
        ],
        [InlineKeyboardButton("💬 Support & Feedback", url='https://t.me/your_support_handle')] # Change this to your handle
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "<b>Welcome to AuraVisual AI</b> 🎨\n\n"
        "Transform your ideas into high-fidelity visuals instantly. "
        "Our AI is ready to create unique images for your projects.\n\n"
        "<b>How to use:</b>\n"
        "Simply type a description of what you want to see (e.g., <i>'A futuristic workspace with neon lighting'</i>) and send it to me!"
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# Optional: Add simple handlers for the buttons so they don't stay "stuck" when clicked
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'help_prompt':
        await query.edit_message_text("Just send me any text message describing an image, and I'll generate it!")
    elif query.data == 'examples':
        await query.edit_message_text("Try prompts like:\n• 'Cyberpunk city in the rain'\n• 'Minimalist logo for a tech startup'\n• '3D render of a golden apple'")
    elif query.data == 'settings':
        await query.edit_message_text("Settings: Defaulting to 1024x1024 (HD). High-performance mode is ON.")
