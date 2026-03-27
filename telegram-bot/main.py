import telebot
from telebot import types
import os

TOKEN = '8585868416:AAH97rTQ_J8JtEcBcswvPqQNcBDV_wXi1nY'
bot = telebot.TeleBot(TOKEN)
IMAGE_PATH = 'bot_image.jpg'

# --- 1. ዋና ማውጫ (Inline Buttons) ---
def main_inline_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛠 አገልግሎቶቻችን", callback_data="go_services"),
        types.InlineKeyboardButton("🏢 ስለ እኛ", callback_data="go_about"),
        types.InlineKeyboardButton("📞 ያግኙን", callback_data="go_contact")
    )
    return markup

# --- 2. ወደ ኋላ መመለሻ ቁልፎች (ሁሌም እንዲኖሩ) ---
def back_buttons(back_to):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("⬅️ ወደ ኋላ ተመለስ", callback_data=back_to),
        types.InlineKeyboardButton("🏠 ወደ ዋና ማውጫ", callback_data="back_to_main")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    # ትልልቆቹን የታች ቁልፎች ለማጥፋት
    remove_kb = types.ReplyKeyboardRemove()
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

    # --- አገልግሎቶች መረጃ ---
    services = {
        "serv_software": "💻 *የሶፍትዌር ማበልጸግ:*\nለድርጅትዎ ልዩ ፍላጎት የተሰሩ የሂሳብ፣ የክምችት እና የአስተዳደር ሲስተሞች።",
        "serv_web": "🌐 *የዌብሳይት ልማት:*\nፈጣን፣ አስተማማኝ እና በስልክም በሚያምር ሁኔታ የሚታዩ ዌብሳይቶች።",
        "serv_mobile": "📱 *የሞባይል መተግበሪያ:*\nለ Android እና iOS የሚሆኑ ዘመናዊ እና ሳቢ መተግበሪያዎች።",
        "serv_it": "🛠 *IT ድጋፍ እና ማማከር:*\nአስተማማኝ የቴክኖሎጂ ምክር እና የቴክኒክ ድጋፍ።",
        "serv_bot": "🤖 *የቴሌግራም ቦቶች:*\nስራዎን የሚያቀልሉ እና ከደንበኞችዎ ጋር የሚያገናኙዎት ዘመናዊ ቦቶች።"
    }

    # --- ስለ እኛ እና እሴቶቻችን ---
    about_text = (
        "👨‍💼 *ሶፎኒያስ ግርማ ገ/ጻዲቅ*\n(መስራች እና ዋና ስራ አስፈጻሚ)\n\n"
        "እንኳን ወደ Sofi System Solution በሰላም መጣችሁ! ድርጅታችን የተመሰረተው የኢትዮጵያን የዲጂታል ጉዞ ወደ ላቀ ደረጃ ለማሸጋገር ነው። አላማችን ተራ የቴክኖሎጂ ውጤቶችን ማቅረብ ሳይሆን፤ የእርስዎን ድርጅት በዘመናዊ ሶፍትዌር በመደገፍ የንግድ ስኬትዎን ማፋጠን ነው።"
    )
    
    values_text = (
        "💎 *የአሰራር እሴቶቻችን:*\n\n"
        "💡 *ቀጣይነት ያለው ፈጠራ:* ሁሌም አዳዲስ ቴክኖሎጂዎችን እና የተሻሉ አሰራሮችን እንተገብራለን።\n\n"
        "🤝 *ፍጹም ታማኝነት:* ግንኙነታችን በግልጽነት እና በታማኝነት ላይ የተመሰረተ ነው።\n\n"
        "🏆 *ጥራት እና ጥንቃቄ:* ስራዎቻችን አለምአቀፍ ደረጃቸውን የጠበቁ እና ከስህተት የጸዱ ናቸው።\n\n"
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
        bot.edit_message_caption(caption=about_text, chat_id=chat_id, 
                                 message_id=message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "about_vision":
        vision = "👁️ *ራዕያችን:*\nበ2030 በኢትዮጵያ የቴክኖሎጂ ኢንደስትሪ ውስጥ ቀዳሚ እና ተመራጭ የዲጂታል መፍትሄ አቅራቢ በመሆን፤ በሚሊዮኖች የሚቆጠሩ ሰዎችን እና ድርጅቶችን ህይወት በቴክኖሎጂ ማዘመን።"
        bot.edit_message_caption(caption=vision, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=back_buttons("go_about"))

    elif call.data == "about_mission":
        mission = "🎯 *ተልዕኳችን:*\nለደንበኞቻችን ፍላጎት ልክ የተበጁ (Custom-tailored)፣ አስተማማኝ እና ዘመናዊ ሶፍትዌሮችን በማልማት፤ የኢትዮጵያ ድርጅቶች በዲጂታል ሽግግር ተወዳዳሪ እና ስኬታማ እንዲሆኑ ማስቻል።"
        bot.edit_message_caption(caption=mission, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=back_buttons("go_about"))

    elif call.data == "about_values":
        bot.edit_message_caption(caption=values_text, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=back_buttons("go_about"))

    elif call.data == "go_contact":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💬 መልዕክት ላክ (Direct Telegram)", url="https://t.me/Sofasofi1"),
            types.InlineKeyboardButton("🏠 ወደ ዋና ማውጫ", callback_data="back_to_main")
        )
        contact = "📞 *ያግኙን (Get In Touch):*\n\n📱 ስልክ: +251 947 35 95 47\n📍 ቦታ: Addis Ababa, Ethiopia\n\nለማንኛውም ጥያቄ ይጻፉልን!"
        bot.edit_message_caption(caption=contact, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=markup)

    elif call.data in services:
        bot.edit_message_caption(caption=services[call.data], chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=back_buttons("go_services"))

    elif call.data == "back_to_main":
        welcome = "👋 እንኳን ወደ *Sofi System Solution* በሰላም መጡ!\n\n🚀 *የዲጂታል ጉዞዎ መጀመሪያ!*"
        bot.edit_message_caption(caption=welcome, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=main_inline_menu())

bot.polling(none_stop=True)