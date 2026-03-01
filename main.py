import telebot
from telebot import types
import urllib.parse
from flask import Flask
import threading
import os
import requests

# --- سيرفر Flask لإبقاء البوت حياً ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- إعدادات البوت ---
API_TOKEN = '8574425507:AAEAXECAtzC-MUJnAGnEBpUe_L-MnNRHUwg'
ADSTERRA_URL = 'https://www.effectivegatecpm.com/tt2p09h6td?key=c8046088eb31ef124f0e28531e06bec0'

bot = telebot.TeleBot(API_TOKEN)

def get_final_url(url):
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        response = session.head(url, allow_redirects=True, timeout=5)
        return str(response.url) # التأكد من تحويله لنص
    except:
        return str(url)

def generate_engine_link(url):
    real_url = get_final_url(url)
    
    # إصلاح الخطأ: التأكد من أننا نتعامل مع نص قبل عمل split
    if isinstance(real_url, list):
        real_url = real_url
        
    clean_url = str(real_url).split("?")
    encoded_url = urllib.parse.quote(clean_url)
    
    if "facebook.com" in clean_url or "fb.watch" in clean_url:
        return f"https://fdown.net/download.php?url={encoded_url}"
    elif "instagram.com" in clean_url:
        return f"https://snapinsta.app/download?url={encoded_url}"
    elif "tiktok.com" in clean_url:
        return f"https://snaptik.app/abc.php?url={encoded_url}"
    else:
        return f"https://en.savefrom.net/results?url={encoded_url}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 **البوت يعمل الآن بنجاح!**\nارسل رابط الفيديو (فيسبوك، إنستغرام، تيك توك) وسأجهز لك رابط التحميل.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup(row_width=1)
        ad_btn = types.InlineKeyboardButton("🔓 1. Unlock Video (Ad)", url=ADSTERRA_URL)
        get_btn = types.InlineKeyboardButton("✅ 2. Get Download Link", callback_data=f"get|{url}")
        markup.add(ad_btn, get_btn)
        bot.send_message(message.chat.id, "🎬 **تم استلام الرابط!**\nاضغط على الزر الأول (إعلان) لدعمنا، ثم الزر الثاني للتحميل:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "⚠️ أرسل رابطاً صحيحاً.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "جاري معالجة الرابط...")
    if "get|" in call.data:
        try:
            video_url = call.data.split("|")
            final_download_page = generate_engine_link(video_url)
            
            bot.send_message(call.message.chat.id, 
                             f"✅ **تم تجهيز الفيديو!**\n\n[📥 اضغط هنا لفتح صفحة التحميل]({final_download_page})\n\n"
                             f"💡 بعد فتح الصفحة، انتظر ثواني واضغط زر Download.", 
                             parse_mode="Markdown")
        except Exception as e:
            bot.send_message(call.message.chat.id, "❌ حدث خطأ بسيط، حاول مرة أخرى.")

bot.remove_webhook()
bot.polling(non_stop=True, skip_pending=True)
