import telebot
from telebot import types
import requests

# بيانات البوت
API_TOKEN = '8574425507:AAFlgLekwiUQtVqRWZZSOtH8MGyt9wJlRz4'
ADSTERRA_URL = 'https://www.effectivegatecpm.com/tt2p09h6td?key=c8046088eb31ef124f0e28531e06bec0'

bot = telebot.TeleBot(API_TOKEN)

# دالة ذكية لاستخراج الروابط باستخدام محرك خارجي (تتجاوز حظر السيرفرات)
def get_universal_link(url):
    try:
        # استخدام محرك Tikwm لتيك توك (الأكثر استقراراً)
        if "tiktok.com" in url:
            api_url = f"https://www.tikwm.com/api/?url={url}"
            res = requests.get(api_url).json()
            return res['data']['play']
        
        # استخدام محرك Cobalt (يدعم يوتيوب، إنستغرام، فيسبوك، تويتر)
        # هذا المحرك مصمم لتجاوز قيود السيرفرات
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {"url": url, "vQuality": "720"}
        res = requests.post("https://api.cobalt.tools/api/json", json=data, headers=headers)
        if res.status_code == 200:
            return res.json().get('url')
            
        return None
    except:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Send me any link (TikTok, YT, IG) to get the direct link.\nأرسل رابط الفيديو للحصول على رابط التحميل المباشر:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup()
        ad_btn = types.InlineKeyboardButton("🔓 Unlock Download Link (Step 1)", url=ADSTERRA_URL)
        check_btn = types.InlineKeyboardButton("✅ Get Direct Link (Step 2)", callback_data=f"get|{url}")
        markup.add(ad_btn)
        markup.add(check_btn)
        
        bot.send_message(message.chat.id, 
                         "🚀 Video is Ready!\n\n1️⃣ Click 'Unlock' (Ad).\n2️⃣ Click 'Get Direct Link'.", 
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Please send a valid link!")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("get|"):
        video_url = call.data.split("|")
        bot.answer_callback_query(call.id, "Bypassing restrictions... Please wait.")
        
        direct_link = get_universal_link(video_url)
        
        if direct_link:
            response = (f"✅ **Success!**\n\n[📥 Click Here to Download / اضغط للتحميل]({direct_link})\n\n"
                       f"💡 *If it opens in browser, long press and 'Save Video'.*")
            bot.send_message(call.message.chat.id, response, parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, "❌ Sorry, this link is highly protected. Try another video or platform.")

bot.polling(non_stop=True, skip_pending=True)
