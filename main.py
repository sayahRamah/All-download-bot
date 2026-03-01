import telebot
from telebot import types
import requests
import http.server
import socketserver
import threading

# 1. فتح منفذ وهمي لإرضاء Render
def start_server():
    port = 10000
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except:
        pass

threading.Thread(target=start_server, daemon=True).start()

# 2. بيانات البوت (التوكن الجديد ورابط الإعلان)
API_TOKEN = '8574425507:AAFlgLekwiUQtVqRWZZSOtH8MGyt9wJlRz4'
ADSTERRA_URL = 'https://www.effectivegatecpm.com/tt2p09h6td?key=c8046088eb31ef124f0e28531e06bec0'

bot = telebot.TeleBot(API_TOKEN)

def get_universal_link(url):
    try:
        # محرك Tikwm لتيك توك
        if "tiktok.com" in url:
            api_url = f"https://www.tikwm.com/api/?url={url}"
            res = requests.get(api_url).json()
            return res['data']['play']
        
        # محرك Cobalt ليوتيوب وإنستغرام وغيرها
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        data = {"url": url, "vQuality": "720"}
        res = requests.post("https://api.cobalt.tools/api/json", json=data, headers=headers)
        if res.status_code == 200:
            return res.json().get('url')
        return None
    except:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Bot is Active!\nأرسل رابط الفيديو للحصول على رابط التحميل المباشر:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup()
        ad_btn = types.InlineKeyboardButton("🔓 Unlock Download Link (Step 1)", url=ADSTERRA_URL)
        check_btn = types.InlineKeyboardButton("✅ Get Direct Link (Step 2)", callback_data=f"get|{url}")
        markup.add(ad_btn)
        markup.add(check_btn)
        
        bot.send_message(message.chat.id, "🚀 Video is Ready!\n\n1️⃣ Click 'Unlock' (Ad).\n2️⃣ Click 'Get Direct Link'.", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Please send a valid link!")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("get|"):
        video_url = call.data.split("|")
        bot.answer_callback_query(call.id, "Extracting... Please wait.")
        
        direct_link = get_universal_link(video_url)
        
        if direct_link:
            bot.send_message(call.message.chat.id, f"✅ **Success!**\n\n[📥 Click Here to Download / اضغط للتحميل]({direct_link})", parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, "❌ Error: This link is protected or not supported.")

# تشغيل البوت مع تجنب التضارب
bot.polling(non_stop=True, skip_pending=True)
