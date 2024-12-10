import os
from flask import Flask, request
import telebot
from telebot import types

# Your bot token (use environment variable for security)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7553752491:AAGpc2EmmoMZk6r5hXS_4TEHwNCTN6iVEm4")  # Set the environment variable for security
bot = telebot.TeleBot(BOT_TOKEN)

# Initialize Flask app
app = Flask(__name__)

# Webhook route
@app.route('/' + BOT_TOKEN, methods=['POST'])
def receive_update():
    json_update = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_update)
    bot.process_new_updates([update])
    return "!", 200

# Set the webhook
@app.route('/')
def webhook_setup():
    bot.remove_webhook()
    # Replace with your Heroku app URL
    webhook_url = f'https://{os.environ.get("HEROKU_APP_NAME")}.herokuapp.com/' + BOT_TOKEN
    bot.set_webhook(url=webhook_url)
    return "Webhook set!", 200

# Start Command Handler
@bot.message_handler(commands=["start"])
def show_main_menu(message):
    chat_id = message.chat.id
    # Main Menu Message
    menu_text = (
        "✨ *Welcome to Dimond™ Products!* ✨\n\n"
        "💎 We are proud to offer premium quality TVs, Speakers, and Software solutions tailored for your needs. "
        "Explore our collections and elevate your lifestyle today! 🛍️\n\n"
        "Please choose a category below to explore:"
    )

    # Create a custom keyboard with each button on its own row
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton("📺 Explore Dimond™ TVs"))
    keyboard.row(types.KeyboardButton("🔊 Discover Dimond™ Speakers"))
    keyboard.row(types.KeyboardButton("💻 Learn About Dimond™ Software"))
    keyboard.row(types.KeyboardButton("ℹ️ Get Help"))

    bot.send_message(chat_id, menu_text, parse_mode="Markdown", reply_markup=keyboard)

# Handle Category Selections
@bot.message_handler(func=lambda message: message.text in ["📺 Explore Dimond™ TVs", "🔊 Discover Dimond™ Speakers", "💻 Learn About Dimond™ Software", "ℹ️ Get Help"])
def handle_categories(message):
    chat_id = message.chat.id
    user_choice = message.text

    if user_choice == "📺 Explore Dimond™ TVs":
        bot.send_message(
            chat_id, 
            "📺 *Dimond™ TVs Collection*\n\nExperience stunning visuals and immersive sound with our premium TVs. "
            "Browse our collection now: [Dimond™ TVs](https://sites.google.com/view/dimond-products/home)",
            parse_mode="Markdown"
        )
    elif user_choice == "🔊 Discover Dimond™ Speakers":
        bot.send_message(
            chat_id, 
            "🔊 *Dimond™ Speakers Collection*\n\nFeel the power of sound like never before. Check out our top-of-the-line speakers here: "
            "[Dimond™ Speakers](https://sites.google.com/view/dimond-products/speakers)",
            parse_mode="Markdown"
        )
    elif user_choice == "💻 Learn About Dimond™ Software":
        bot.send_message(
            chat_id,
            "💻 *Dimond™ Software Solutions*\n\nUpgrade your digital experience with our cutting-edge software. "
            "Explore more details here: [Dimond™ Software](https://sites.google.com/view/dimond-products/home)",
            parse_mode="Markdown"
        )
    elif user_choice == "ℹ️ Get Help":
        bot.send_message(
            chat_id,
            "ℹ️ *Need Assistance?*\n\n"
            "📞 *Phone:* +251 911 123 456\n"
            "📧 *Email:* support@diamond.et\n"
            "📍 *Location:* Addis Ababa, Ethiopia\n\n"
            "💬 *Our friendly team is here to help! Don’t hesitate to reach out to us.*",
            parse_mode="Markdown"
        )

# Block Typing (Catch-all for unexpected inputs)
@bot.message_handler(func=lambda message: True)
def block_typing(message):
    chat_id = message.chat.id
    # Notify user
    bot.send_message(
        chat_id,
        "⛔️ *Oops! Typing is disabled.* Please use the buttons below to navigate the menu and explore our products.",
        parse_mode="Markdown"
    )

    # Re-display the main menu keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton("📺 Explore Dimond™ TVs"))
    keyboard.row(types.KeyboardButton("🔊 Discover Dimond™ Speakers"))
    keyboard.row(types.KeyboardButton("💻 Learn About Dimond™ Software"))
    keyboard.row(types.KeyboardButton("ℹ️ Get Help"))
    bot.send_message(chat_id, "👇 *Choose an option below:*", reply_markup=keyboard, parse_mode="Markdown")

# Running the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
