import telebot
from telebot import types
import os
from flask import Flask
import threading

# 1. የቦት መረጃ (Token)
TOKEN = '8585868416:AAH97rTQ_J8JtEcBcswvPqQNcBDV_wXi1nY'
bot = telebot.TeleBot(TOKEN)
IMAGE_PATH = 'bot_image.jpg' # በ GitHub ላይ ያለህ የፎቶ ስም

# 2. ለ Render አስፈላጊ የሆነ ሰርቨር (ቦቱ እንዳይዘጋ)
app = Flask(__name__)

@app.route('/')
def index():
    return "Sofi System Solution Bot is Live!", 200

# --- 3. የቁልፎች ዝግጅት (Keyboards) ---

def main_inline_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛠 አገልግሎቶቻችን", callback_data="go_services"),
        types.InlineKeyboardButton("🏢 ስለ እኛ", callback_data="go_about"),
        types.InlineKeyboardButton("📞 ያግኙን", callback_data="go_contact")
    )
    return markup

def back_buttons(back_to):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("⬅️ ወደ ኋላ ተመለስ", callback_data=back_to),
        types.InlineKeyboardButton("🏠 ወደ ዋና ማውጫ", callback_data="back_to_main")
    )
    return markup

# --- 4. የቦቱ ምላሾች (Handlers) ---

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "Sofi System Solution\nTechnology Excellence\n\n"
        "🚀 *የዲጂታል ጉዞዎ መጀመሪያ!*\n\n"
        "ጥራቱን የጠበቀ ዌብሳይት፣ ሞባይል አፕ እና ዘመናዊ ሶፍትዌሮችን በማልማት የድርጅትዎን ስኬት እናፋጥናለን።"
    )
    if os.path.exists(IMAGE_PATH):
        with open(IMAGE_PATH, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=welcome_text, 
                           parse_mode="Markdown", reply_markup=main_inline_menu())
    else:
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", 
                         reply_markup=main_inline_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    services = {
        "serv_software": "💻 *የሶፍትዌር ማበልጸግ:*\nለድርጅትዎ ልዩ ፍላጎት የተሰሩ የሂሳብ፣ የክምችት እና የአስተዳደር ሲስተሞች።",
        "serv_web": "🌐 *የዌብሳይት ልማት:*\nፈጣን፣ አስተማማኝ እና በስልክም በሚያምር ሁኔታ የሚታዩ ዌብሳይቶች።",
        "serv_mobile": "📱 *የሞባይል መተግበሪያ:*\nለ Android እና iOS የሚሆኑ ዘመናዊ እና ሳቢ መተግበሪያዎች።",
        "serv_it": "🛠 *IT ድጋፍ እና ማማከር:*\nአስተማማኝ የቴክኖሎጂ ምክር እና የቴክኒክ ድጋፍ።",
        "serv_bot": "🤖 *የቴሌግራም ቦቶች:*\nስራዎን የሚያቀልሉ እና ከደንበኞችዎ ጋር የሚያገናኙዎት ዘመናዊ ቦቶች።"
    }

    if call.data == "go_services":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💻 የሶፍትዌር ማበልጸግ", callback_data="serv_software"),
            types.InlineKeyboardButton("🌐 የዌብሳይት ልማት", callback_data="serv_web"),
            types.InlineKeyboardButton("📱 የሞባይል መተግበሪያ", callback_data="serv_mobile"),
            types.InlineKeyboardButton("🛠 IT ድጋፍ እና ማማከር", callback_data="serv_it"),
            types.InlineKeyboardButton("🤖 የቴሌግራም ቦቶች", callback_data="serv_bot"),
            types.InlineKeyboardButton("🏠 ወደ ዋና ማውጫ", callback_data="back_to_main")
        )
        bot.edit_message_caption(caption="💻 *የምንሰጣቸው አገልግሎቶች:*", chat_id=chat_id, 
                                 message_id=message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "go_contact":
        markup = types.InlineKeyboardMarkup(row_width=1)
        # የአንተ ሊንኮች እዚህ ገብተዋል
        markup.add(
            types.InlineKeyboardButton("🔵 Facebook Page", url="https://www.facebook.com/profile.php?id=61578429291197"),
            types.InlineKeyboardButton("📢 Telegram Channel", url="https://t.me/sofi_system_solution"),
            types.InlineKeyboardButton("🤖 Information Bot", url="https://t.me/Sofi_System_Solution_INFObot"),
            types.InlineKeyboardButton("💬 Direct Message", url="https://t.me/Sofasofi1"),
            types.InlineKeyboardButton("🏠 ወደ ዋና ማውጫ", callback_data="back_to_main")
        )
        contact_text = (
            "📞 *ያግኙን (Get In Touch):*\n\n"
            "📱 ስልክ: +251 947 35 95 47\n"
            "📍 ቦታ: Addis Ababa, Ethiopia\n"
            "📧 ኢሜይል: sofonyasg@gmail.com\n\n"
            "ከታች ያሉትን አዝራሮች በመጫን በሶሻል ሚዲያ ያግኙን! 👇"
        )
        bot.edit_message_caption(caption=contact_text, chat_id=chat_id, 
                                 message_id=message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "go_about":
        about_text = "👨‍💼 *Sofi System Solution*\n\nየኢትዮጵያን የዲጂታል ጉዞ ወደ ላቀ ደረጃ ለማሸጋገር የተመሰረተ ድርጅት ነው። ጥራት እና ታማኝነት መርሀችን ነው።"
        bot.edit_message_caption(caption=about_text, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=back_buttons("back_to_main"))

    elif call.data in services:
        bot.edit_message_caption(caption=services[call.data], chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=back_buttons("go_services"))

    elif call.data == "back_to_main":
        bot.edit_message_caption(caption="👋 እንኳን ወደ *Sofi System Solution* በሰላም መጡ!", 
                                 chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=main_inline_menu())

# --- 5. ማስጀመሪያ (Runner) ---
def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
