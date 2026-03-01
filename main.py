import telebot
from telebot import types
import urllib.parse
from flask import Flask
import threading
import os

# --- تشغيل Flask لضمان استقرار Render ---
app = Flask(__name__)
@app.route('/')
def home(): return "Downloader Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- إعدادات البوت ---
API_TOKEN = '8574425507:AAEAXECAtzC-MUJnAGnEBpUe_L-MnNRHUwg'
ADSTERRA_URL = 'https://www.effectivegatecpm.com/tt2p09h6td?key=c8046088eb31ef124f0e28531e06bec0'

bot = telebot.TeleBot(API_TOKEN)

def get_final_downloader(url):
    encoded_url = urllib.parse.quote(url)
    
    # محرك إنستغرام وفيسبوك المتقدم
    if "instagram.com" in url or "facebook.com" in url or "fb.watch" in url:
        return f"https://fdown.net/download.php?url={encoded_url}"
    
    # محرك تيك توك بدون علامة مائية
    elif "tiktok.com" in url:
        return f"https://snaptik.app/abc.php?url={encoded_url}"
    
    # محرك يوتيوب المستقر
    elif "youtube.com" in url or "youtu.be" in url:
        return f"https://en.savefrom.net/1-youtube-video-downloader-521/v7/?url={encoded_url}"
    
    # محرك شامل لأي موقع آخر
    else:
        return f"https://www.google.com/search?q=download+video+from+{encoded_url}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 أهلاً بك في بوت التحميل العالمي!\n\nيدعم الآن بكفاءة:\n✅ Facebook & FB Watch\n✅ Instagram Reels & Video\n✅ TikTok (No Watermark)\n✅ YouTube HD\n\nأرسل الرابط الآن لبدء التحميل:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup(row_width=1)
        # زر الربح من Adsterra
        ad_btn = types.InlineKeyboardButton("🔓 1. Unlock Download (Support Us)", url=ADSTERRA_URL)
        # زر الانتقال لصفحة التحميل الحقيقية
        get_btn = types.InlineKeyboardButton("✅ 2. Get Video Link", callback_data=f"get|{url}")
        markup.add(ad_btn, get_btn)
        
        bot.send_message(message.chat.id, "🎬 تم فحص الرابط بنجاح!\n\nيرجى الضغط على الزر الأول لدعمنا (إعلان)، ثم الزر الثاني لاستلام الفيديو:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "⚠️ يرجى إرسال رابط صحيح يبدأ بـ http")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "جاري تحضير الرابط المباشر...")
    if "get|" in call.data:
        video_url = call.data.split("|")
        final_link = get_final_downloader(video_url)
        
        bot.send_message(call.message.chat.id, 
                         f"✅ **الرابط جاهز للتحميل!**\n\n[📥 اضغط هنا لبدء التنزيل]({final_link})\n\n"
                         f"💡 *بعد فتح الصفحة، اضغط على زر 'Download' الموجود في الموقع.*", 
                         parse_mode="Markdown")

# حل مشكلة Conflict 409
bot.remove_webhook()
bot.polling(non_stop=True, skip_pending=True)
