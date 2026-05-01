import os
import telebot
from telebot import types

# Use your token here directly to avoid the 'NoneType' error from earlier
API_TOKEN = "8650108155:AAFCF52LC3NRDCfgYXjo3U8Lq6ZUeZGIi8Y" 
OFFER_URL = "https://playfulcaphigh.com/?sub2=ustegram"

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_offer(message):
    # Create a high-conversion button
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💰 Claim Your Free Reward Now", url=OFFER_URL)
    markup.add(btn)

    # Direct copy focused on the Freecash offer
    text = (
        "🔥 **Exclusive Offer Unlocked!**\n\n"
        "You've been invited to join our premium rewards portal. "
        "Complete simple tasks and start earning instantly.\n\n"
        "👇 **Click the button below to start:**"
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def redirect_all(message):
    # Redirect even if they type something else
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ Continue to Offer", url=OFFER_URL)
    markup.add(btn)
    
    bot.send_message(
        message.chat.id, 
        "To proceed, please use the verified link below:", 
        reply_markup=markup
    )

if __name__ == "__main__":
    bot.infinity_polling()
