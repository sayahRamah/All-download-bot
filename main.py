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
def home(): return "All Video Downloader is Active!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- إعدادات البوت ---
API_TOKEN = '8574425507:AAEAXECAtzC-MUJnAGnEBpUe_L-MnNRHUwg'
ADSTERRA_URL = 'https://www.effectivegatecpm.com/tt2p09h6td?key=c8046088eb31ef124f0e28531e06bec0'

bot = telebot.TeleBot(API_TOKEN)

def get_real_url(url):
    """دالة لفك الروابط المختصرة وجلب الرابط الأصلي"""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except:
        return url

def get_final_downloader(url):
    # 1. جلب الرابط الأصلي (خاصة لروابط الفيسبوك المختصرة)
    real_url = get_real_url(url)
    
    # 2. تنظيف الرابط من زوائد التتبع
    clean_url = real_url.split("?")
    encoded_url = urllib.parse.quote(clean_url)
    
    # محرك فيسبوك المتطور (SnapSave هو الأفضل لروابط r/share)
    if "facebook.com" in clean_url or "fb.watch" in clean_url:
        return f"https://snapsave.app/details?url={encoded_url}"
    
    # محرك إنستغرام (SnapInsta)
    elif "instagram.com" in clean_url:
        return f"https://snapinsta.app/download?url={encoded_url}"
    
    # محرك تيك توك
    elif "tiktok.com" in clean_url:
        return f"https://snaptik.app/abc.php?url={encoded_url}"
    
    # محرك يوتيوب
    elif "youtube.com" in clean_url or "youtu.be" in clean_url:
        return f"https://en.savefrom.net/1-youtube-video-downloader-521/v7/?url={encoded_url}"
    
    else:
        return f"https://en.savefrom.net/results?url={encoded_url}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 أهلاً بك! بوت التحميل يدعم الآن روابط الفيسبوك والإنستغرام الجديدة.\n\nأرسل الرابط الآن:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup(row_width=1)
        ad_btn = types.InlineKeyboardButton("🔓 1. Unlock Download (Ad)", url=ADSTERRA_URL)
        get_btn = types.InlineKeyboardButton("✅ 2. Get Video Link", callback_data=f"get|{url}")
        markup.add(ad_btn, get_btn)
        bot.send_message(message.chat.id, "🎬 تم استلام الرابط!\n\nاضغط على الزر الأول (إعلان) لدعمنا، ثم الزر الثاني للتحميل:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "⚠️ يرجى إرسال رابط صحيح.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "جاري استخراج الرابط الأصلي...")
    if "get|" in call.data:
        video_url = call.data.split("|")
        final_link = get_final_downloader(video_url)
        
        bot.send_message(call.message.chat.id, 
                         f"✅ **الرابط جاهز!**\n\n[📥 اضغط هنا للتحميل]({final_link})\n\n"
                         f"💡 *سيفتح لك موقع SnapSave، انتظر ثانية واضغط على زر Download الأخضر.*", 
                         parse_mode="Markdown")

bot.remove_webhook()
bot.polling(non_stop=True, skip_pending=True)
