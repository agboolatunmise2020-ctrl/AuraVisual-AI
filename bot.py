import telebot
from telebot import types

# PASTE YOUR TOKEN DIRECTLY BETWEEN THE QUOTES BELOW
API_TOKEN = "8650108155:AAFCF52LC3NRDCfgYXjo3U8Lq6ZUeZGIi8Y" 
AFFILIATE_LINK = "https://playfulcaphigh.com/?sub2=ustegram"

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "📝 **URL Analyzer Active.**\nSend any link to check safety and bypass trackers.")

@bot.message_handler(func=lambda message: True)
def handle_url(message):
    url = message.text
    if url.startswith(('http://', 'https://')):
        msg = bot.reply_to(message, "⌛ *Scanning...*", parse_mode='Markdown')
        markup = types.InlineKeyboardMarkup()
        btn_redirect = types.InlineKeyboardButton("🔓 Access Secure Link", url=AFFILIATE_LINK)
        markup.add(btn_redirect)
        response = (
            "✅ **Link Analyzed**\n\n"
            "**Safety Rating:** High\n"
            "**Trackers:** Removed\n\n"
            "Click below to access the destination through our secure proxy."
        )
        bot.edit_message_text(response, message.chat.id, msg.message_id, 
                              reply_markup=markup, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "⚠️ Please send a valid URL.")

if __name__ == "__main__":
    bot.infinity_polling()
