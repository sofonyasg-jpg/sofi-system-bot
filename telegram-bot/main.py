import telebot
from telebot import types
import os
from flask import Flask
import threading

# 1. የቦት መረጃ (Token)
TOKEN = '8585868416:AAH97rTQ_J8JtEcBcswvPqQNcBDV_wXi1nY'
bot = telebot.TeleBot(TOKEN)
IMAGE_PATH = 'bot_image.jpg'

# 2. ለ Render አስፈላጊ የሆነ ሰርቨር
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

    # አገልግሎቶች ዝርዝር
    services = {
        "serv_software": "💻 *የሶፍትዌር ማበልጸግ:*\nለድርጅትዎ ልዩ ፍላጎት የተሰሩ የሂሳብ፣ የክምችት እና የአስተዳደር ሲስተሞች።",
        "serv_web": "🌐 *የዌብሳይት ልማት:*\nፈጣን፣ አስተማማኝ እና በስልክም በሚያምር ሁኔታ የሚታዩ ዌብሳይቶች።",
        "serv_mobile": "📱 *የሞባይል መተግበሪያ:*\nለ Android እና iOS የሚሆኑ ዘመናዊ እና ሳቢ መተግበሪያዎች።",
        "serv_it": "🛠 *IT ድጋፍ እና ማማከር:*\nአስተማማኝ የቴክኖሎጂ ምክር እና የቴክኒክ ድጋፍ።",
        "serv_bot": "🤖 *የቴሌግራም ቦቶች:*\nስራዎን የሚያቀልሉ እና ከደንበኞችዎ ጋር የሚያገናኙዎት ዘመናዊ ቦቶች።"
    }

    # ስለ እኛ መረጃ
    about_intro = (
        "👨‍💼 *ሶፎኒያስ ግርማ ገ/ጻዲቅ*\n(መስራች እና ዋና ስራ አስፈጻሚ)\n\n"
        "እንኳን ወደ Sofi System Solution በሰላም መጣችሁ! ድርጅታችን የተመሰረተው የኢትዮጵያን የዲጂታል ጉዞ ወደ ላቀ ደረጃ ለማሸጋገር ነው። አላማችን ተራ የቴክኖሎጂ ውጤቶችን ማቅረብ ሳይሆን፤ የእርስዎን ድርጅት በዘመናዊ ሶፍትዌር በመደገፍ የንግድ ስኬትዎን ማፋጠን ነው።"
    )

    values_text = (
        "💎 *የአሰራር እሴቶቻችን:*\n\n"
        "💡 *ቀጣይነት ያለው ፈጠራ:* ሁሌም አዳዲስ ቴክኖሎጂዎችን እና የተሻሉ አሰራሮችን እንተገብራለን።\n\n"
        "🤝 *ፍጹም ታማኝነት:* ግንኙነታችን በግልጽነት እና በታማኝነት ላይ የተመሰረተ ነው።\n\n"
        "🏆 *ጥራት እና ጥንቃቄ:* ስራዎቻችን አለምአቀፍ ደረጃቸውን የጠበቁ ናቸው።\n\n"
        "❤️ *ደንበኛ ተኮር አገልግሎት:* ዘላቂ የሆነ የቴክኒክ ድጋፍ እንሰጣለን።\n\n"
        "🌍 *ዲጂታል ተደራሽነት:* ተመጣጣኝ ዋጋን ከጥራት ጋር እናቀርባለን።"
    )

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

    elif call.data == "go_about":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("👁️ ራዕያችን", callback_data="about_vision"),
            types.InlineKeyboardButton("🎯 ተልዕኳችን", callback_data="about_mission"),
            types.InlineKeyboardButton("✨ እሴቶቻችን", callback_data="about_values"),
            types.InlineKeyboardButton("🏠 ወደ ዋና ማውጫ", callback_data="back_to_main")
        )
        bot.edit_message_caption(caption=about_intro, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=markup)

    elif call.data == "about_vision":
        vision = "👁️ *ራዕያችን:*\nበ2030 በኢትዮጵያ የቴክኖሎጂ ኢንደስትሪ ውስጥ ቀዳሚ እና ተመራጭ የዲጂታል መፍትሄ አቅራቢ በመሆን፤ ህይወትን በቴክኖሎጂ ማዘመን።"
        bot.edit_message_caption(caption=vision, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=back_buttons("go_about"))

    elif call.data == "about_mission":
        mission = "🎯 *ተልዕኳችን:*\nለደንበኞቻችን ፍላጎት ልክ የተበጁ፣ አስተማማኝ እና ዘመናዊ ሶፍትዌሮችን በማልማት፤ የኢትዮጵያ ድርጅቶች በዲጂታል ሽግግር ስኬታማ እንዲሆኑ ማስቻል።"
        bot.edit_message_caption(caption=mission, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=back_buttons("go_about"))

    elif call.data == "about_values":
        bot.edit_message_caption(caption=values_text, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=back_buttons("go_about"))

    elif call.data == "go_contact":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💬 መልዕክት ላክ (Telegram)", url="https://t.me/Sofasofi1"),
            types.InlineKeyboardButton("🏠 ወደ ዋና ማውጫ", callback_data="back_to_main")
        )
        contact = "📞 *ያግኙን (Get In Touch):*\n\n📱 ስልክ: +251 947 35 95 47\n📍 ቦታ: Addis Ababa, Ethiopia\n📧 ኢሜይል: sofonyasg@gmail.com"
        bot.edit_message_caption(caption=contact, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=markup)

    elif call.data in services:
        bot.edit_message_caption(caption=services[call.data], chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=back_buttons("go_services"))

    elif call.data == "back_to_main":
        welcome = "👋 እንኳን ወደ *Sofi System Solution* በሰላም መጡ!\n\n🚀 *የዲጂታል ጉዞዎ መጀመሪያ!*"
        bot.edit_message_caption(caption=welcome, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=main_inline_menu())

# --- 5. ማስጀመሪያ (Runner) ---

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # ቦቱን በሌላ Thread ማስጀመር
    threading.Thread(target=run_bot).start()
    
    # ሰርቨሩን ለ Render ማስጀመር (Port 10000 ለ Render default ነው)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
