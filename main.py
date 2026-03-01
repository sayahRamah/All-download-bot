import telebot
from telebot import types
import urllib.parse
from flask import Flask
import threading
import os
import requests

# --- تشغيل سيرفر Flask لضمان بقاء البوت حياً على Render ---
app = Flask(__name__)
@app.route('/')
def home(): return "Downloader Engine is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- إعدادات البوت ---
API_TOKEN = '8574425507:AAEAXECAtzC-MUJnAGnEBpUe_L-MnNRHUwg'
ADSTERRA_URL = 'https://www.effectivegatecpm.com/tt2p09h6td?key=c8046088eb31ef124f0e28531e06bec0'

bot = telebot.TeleBot(API_TOKEN)

def get_final_url(url):
    """فك الروابط المختصرة وروابط المشاركة (Facebook/Instagram)"""
    try:
        session = requests.Session()
        # تظاهر بأنك متصفح عادي لتجنب الحظر
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        response = session.head(url, allow_redirects=True, timeout=5)
        return response.url
    except:
        return url

def generate_engine_link(url):
    # 1. الحصول على الرابط الحقيقي (فك Redirect)
    real_url = get_final_url(url)
    # 2. تنظيف الرابط من التتبع
    clean_url = real_url.split("?")
    encoded_url = urllib.parse.quote(clean_url)
    
    # توزيع الروابط على أقوى المحركات المتخصصة
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
    bot.reply_to(message, "🚀 **مرحباً بك في النسخة الاحترافية!**\nارسل رابط (فيسبوك، إنستغرام، تيك توك) وسأجهز لك رابط التحميل فوراً.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup(row_width=1)
        # زر الإعلان للربح (أدسيرا)
        ad_btn = types.InlineKeyboardButton("🔓 1. Unlock Video (Support Us)", url=ADSTERRA_URL)
        # زر جلب الفيديو
        get_btn = types.InlineKeyboardButton("✅ 2. Get Download Link", callback_data=f"get|{url}")
        markup.add(ad_btn, get_btn)
        bot.send_message(message.chat.id, "🎬 **تم استلام الرابط!**\nللحصول على الفيديو، اتبع الخطوتين بالأسفل:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "⚠️ أرسل رابطاً صحيحاً.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "جاري فك التشفير وتجهيز الرابط...")
    if "get|" in call.data:
        video_url = call.data.split("|")
        final_download_page = generate_engine_link(video_url)
        
        bot.send_message(call.message.chat.id, 
                         f"✅ **تم تجهيز الفيديو بنجاح!**\n\n[📥 اضغط هنا لفتح صفحة التحميل]({final_download_page})\n\n"
                         f"💡 **طريقة التحميل:**\nستفتح لك صفحة المحرك، انتظر ثواني ثم اضغط على الزر الأخضر (Download).", 
                         parse_mode="Markdown")

bot.remove_webhook()
bot.polling(non_stop=True, skip_pending=True)
