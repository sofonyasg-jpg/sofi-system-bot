import telebot
from telebot import types
import os
from flask import Flask
import threading
import re

# 1. የቦት መረጃ (Token)
TOKEN = '8585868416:AAH97rTQ_J8JtEcBcswvPqQNcBDV_wXi1nY'
bot = telebot.TeleBot(TOKEN)

# 2. የፎቶ መገኛ መንገድ (Path)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, 'bot_image.JPG')

# 3. Flask ሰርቨር (ለ Render)
app = Flask(__name__)

@app.route('/')
def index():
    return "Sofi System Solution Bot is Live!", 200

# --- 4. የቁልፎች ዝግጅት (Keyboards) ---

def main_inline_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛠 አገልግሎቶቻችን", callback_data="go_services"),
        types.InlineKeyboardButton("🏢 ስለ እኛ (ራዕይ/ተልዕኮ)", callback_data="go_about"),
        types.InlineKeyboardButton("📞 ያግኙን", callback_data="go_contact")
    )
    return markup

def back_buttons(back_to):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("⬅️ ወደ ኋላ", callback_data=back_to),
        types.InlineKeyboardButton("🏠 ዋና ማውጫ", callback_data="back_to_main")
    )
    return markup

# --- 5. የቦቱ ምላሾች (Handlers) ---

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "🚀 *እንኳን ወደ Sofi System Solution በሰላም መጡ!*\n\n"
        "እኛ በዘመናዊ ቴክኖሎጂ የታገዘ መፍትሄ ለቢዝነስዎ የምንሰጥ ታማኝ አጋርዎ ነን። "
        "የእርስዎ ስኬት የእኛም ስኬት ነው። በዲጂታሉ ዓለም ተወዳዳሪ እንዲሆኑ በቁርጠኝነት እንሰራለን!\n\n"
        "— *ሶፎኒያስ ግርማ (Sofi)*, Founder & Lead Developer"
    )
    
    try:
        if os.path.exists(IMAGE_PATH):
            with open(IMAGE_PATH, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=welcome_text, 
                               parse_mode="Markdown", reply_markup=main_inline_menu())
        else:
            bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", 
                             reply_markup=main_inline_menu())
    except Exception:
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", 
                         reply_markup=main_inline_menu())

# ከዌብሳይት የሚመጣውን መልዕክት ለይቶ ምላሽ መስጫ አዝራር ማዘጋጀት
@bot.message_handler(func=lambda message: "አዲስ መልዕክት ከዌብሳይት" in message.text)
def web_message_reply_handler(message):
    # ኢሜይሉን ከጽሑፉ ውስጥ ፈልጎ ማውጣት
    email_match = re.search(r'📧 \*\*ኢሜይል:\*\* ([\w\.-]+@[\w\.-]+\.\w+)', message.text)
    user_email = email_match.group(1) if email_match else None

    markup = types.InlineKeyboardMarkup()
    if user_email:
        reply_button = types.InlineKeyboardButton(
            "📧 በኢሜይል መልስ ስጥ", 
            url=f"mailto:{user_email}"
        )
        markup.add(reply_button)
    
    bot.reply_to(message, "ለዚህ ደንበኛ መልስ ለመስጠት ከታች ያለውን አዝራር ይጫኑ፡", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    def safe_edit(text, markup):
        try:
            bot.edit_message_caption(caption=text, chat_id=chat_id, message_id=message_id, 
                                     parse_mode="Markdown", reply_markup=markup)
        except:
            bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, 
                                 parse_mode="Markdown", reply_markup=markup)

    # ሰፊ የአገልግሎቶች ማብራሪያ
    services_data = {
        "serv_web": (
            "🌐 *የዌብሳይት ልማት (Web Development)*\n\n"
            "• ለማንኛውም ቢዝነስ የሚሆኑ ፈጣን፣ ደህንነታቸው የተጠበቀ እና በስልክም በሚያምር ሁኔታ የሚታዩ (Responsive) ዌብሳይቶች።\n"
            "• ከቀላል ማስተዋወቂያ ድረ-ገጾች (Landing Pages) እስከ ውስብስብ የንግድ ዌብሳይቶች (E-commerce) እንሰራለን።\n"
            "• *ልዩነታችን:* ዌብሳይቶቻችን SEO Friendly (ጎግል ላይ በቀላሉ የሚገኙ) እና እጅግ ፈጣን ናቸው።"
        ),
        "serv_mobile": (
            "📱 *የሞባይል መተግበሪያ (Mobile App)*\n\n"
            "• ለ Android እና iOS ስልኮች የሚሆኑ ዘመናዊ እና ለተጠቃሚ ምቹ የሆኑ መተግበሪያዎች።\n"
            "• *ልዩነታችን:* ደንበኞች በቀላሉ ሊጠቀሙት የሚችሉ (UI/UX) እና ከፍተኛ ደህንነት ያላቸው አፖችን እንገነባለን።"
        ),
        "serv_hr": (
            "👥 *HR & Payroll Management System*\n\n"
            "• *ለመንግስት እና ለግል መሥሪያ ቤቶች* የሚሆን ማንኛውንም የሲስተም ስራ በብቃት እንሰራለን።\n"
            "• የሰራተኞች መረጃ አስተዳደር፣ የደመወዝ ክፍያ፣ የዕረፍት እና የቅጥር ቁጥጥርን በዲጂታል መንገድ ያቀላጥፋል።\n"
            "• የወረቀት ስራን በማስቀረት መረጃን በቅጽበት ለማግኘት ይረዳል።"
        ),
        "serv_soft": (
            "💻 *የሶፍትዌር ማበልጸግ (Software Development)*\n\n"
            "• የሂሳብ መቆጣጠሪያ (Accounting)፣ የንብረትና የመጋዘን አስተዳደር (Inventory) ሲስተሞች።\n"
            "• የድርጅትዎን ውስጣዊ አሰራር የሚቆጣጠሩ እና ስራን የሚያቀልሉ ዘመናዊ ሶፍትዌሮች።"
        ),
        "serv_bot": (
            "🤖 *የቴሌግራም ቦቶች (Telegram Bots)*\n\n"
            "• ደንበኞችን 24 ሰዓት ያለ እረፍት በራስ-ሰር የሚያስተናግዱ (Auto-reply) ቦቶች።\n"
            "• ምርት የሚሸጡ፣ መረጃ የሚሰበስቡ ወይም የቢሮ ስራን የሚያቀልሉ ቦቶች።"
        )
    }

    if call.data == "go_services":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🌐 የዌብሳይት ልማት", callback_data="serv_web"),
            types.InlineKeyboardButton("📱 የሞባይል መተግበሪያ", callback_data="serv_mobile"),
            types.InlineKeyboardButton("👥 HR & Payroll (መንግስት/ግል)", callback_data="serv_hr"),
            types.InlineKeyboardButton("💻 የሶፍትዌር ማበልጸግ", callback_data="serv_soft"),
            types.InlineKeyboardButton("🤖 የቴሌግራም ቦቶች", callback_data="serv_bot"),
            types.InlineKeyboardButton("🏠 ዋና ማውጫ", callback_data="back_to_main")
        )
        safe_edit("🛠 *የምንሰጣቸው አገልግሎቶች:*", markup)

    elif call.data in services_data:
        safe_edit(services_data[call.data], back_buttons("go_services"))

    elif call.data == "go_about":
        about_text = (
            "🏢 *ስለ Sofi System Solution*\n\n"
            "🎯 *ተልዕኮ:* ጥራቱን የጠበቀ የሶፍትዌር ውጤቶችን በማቅረብ የድርጅቶችን አሰራር ማዘመን እና ምርታማነትን ማሳደግ።\n\n"
            "👁 *ራዕይ:* በ2030 በኢትዮጵያ ቀዳሚው እና ተመራጭ የቴክኖሎጂ መፍትሄ አቅራቢ ድርጅት መሆን።\n\n"
            "💎 *እሴቶች:* ታማኝነት፣ ጥራት እና ፈጠራ!"
        )
        safe_edit(about_text, back_buttons("back_to_main"))

    elif call.data == "go_contact":
        contact_text = (
            "📞 *ያግኙን (Contact Us)*\n\n"
            "📱 ስልክ: +251 947 35 95 47\n"
            "📧 ኢሜይል: sofonyasg@gmail.com\n"
            "📍 ቦታ: Addis Ababa, Ethiopia\n\n"
            "🔗 *ማህበራዊ ሚዲያ:* [Facebook](https://www.facebook.com/profile.php?id=61578429291197) | [Telegram](https://t.me/sofi_system_solution)"
        )
        safe_edit(contact_text, back_buttons("back_to_main"))

    elif call.data == "back_to_main":
        safe_edit("👋 እንኳን ወደ *Sofi System Solution* በሰላም መጡ!", main_inline_menu())

# --- 6. ማስጀመሪያ ---
def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # ቦቱን በሌላ Thread ማስጀመር (ለ Render ፍጥነት)
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
