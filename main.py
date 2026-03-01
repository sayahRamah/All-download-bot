import telebot
from telebot import types
import urllib.parse
from flask import Flask
import threading
import os

# --- تشغيل سيرفر Flask لإرضاء Render ---
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

def generate_smart_link(url):
    encoded_url = urllib.parse.quote(url)
    
    # تحويل ذكي بناءً على نوع المنصة
    if "facebook.com" in url or "fb.watch" in url:
        return f"https://snapsave.app/details?url={encoded_url}"
    elif "instagram.com" in url:
        return f"https://igdownloader.app/download?url={encoded_url}"
    elif "tiktok.com" in url:
        return f"https://snaptik.app/abc.php?url={encoded_url}"
    elif "youtube.com" in url or "youtu.be" in url:
        return f"https://en.savefrom.net/1-youtube-video-downloader-521/v7/?url={encoded_url}"
    else:
        return f"https://en.savefrom.net/results?url={encoded_url}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 أهلاً بك! أنا بوت التحميل الشامل.\nيدعم الآن: (Facebook, Instagram, TikTok, YouTube)\n\nأرسل الرابط الآن:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup(row_width=1)
        # زر الإعلان للربح
        ad_btn = types.InlineKeyboardButton("🔓 1. Unlock Link (Support Us)", url=ADSTERRA_URL)
        # زر جلب الرابط الحقيقي
        check_btn = types.InlineKeyboardButton("✅ 2. Get Video Link", callback_data=f"get|{url}")
        markup.add(ad_btn, check_btn)
        
        bot.send_message(message.chat.id, "🎬 تم استلام الرابط بنجاح!\n\nاضغط على الزر الأول لدعمنا، ثم الزر الثاني للتحميل:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "⚠️ عذراً، أرسل رابطاً صحيحاً يبدأ بـ http")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "جاري تجهيز الرابط...")
    if "get|" in call.data:
        video_url = call.data.split("|")
        final_link = generate_smart_link(video_url)
        
        bot.send_message(call.message.chat.id, 
                         f"✅ **تم استخراج الرابط بنجاح!**\n\n[📥 اضغط هنا لبدء التحميل]({final_link})\n\n"
                         f"💡 *ملاحظة: عند فتح الصفحة، اضغط على زر Download المتاح هناك.*", 
                         parse_mode="Markdown")

bot.remove_webhook()
bot.polling(non_stop=True, skip_pending=True)
