import telebot
from telebot import types
import urllib.parse
from flask import Flask
import threading
import os

# --- جزء السيرفر لإبقاء البوت حياً (Flask) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    # Render يحتاج لقراءة الـ PORT ليعتبر السيرفر ناجحاً
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# تشغيل Flask في خيط منفصل
threading.Thread(target=run_flask, daemon=True).start()

# --- إعدادات البوت ---
API_TOKEN = '8574425507:AAEAXECAtzC-MUJnAGnEBpUe_L-MnNRHUwg'
ADSTERRA_URL = 'https://www.effectivegatecpm.com/tt2p09h6td?key=c8046088eb31ef124f0e28531e06bec0'

bot = telebot.TeleBot(API_TOKEN)

def generate_download_link(url):
    encoded_url = urllib.parse.quote(url)
    if "tiktok.com" in url:
        return f"https://snaptik.app/abc.php?url={encoded_url}"
    elif "youtube.com" in url or "youtu.be" in url:
        return f"https://en.savefrom.net/1-youtube-video-downloader-521/v7/?url={encoded_url}"
    else:
        return f"https://en.savefrom.net/results?url={encoded_url}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "⚡️ البوت يعمل الآن بكفاءة عالية!\nأرسل رابط الفيديو الذي تريد تحميله:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup(row_width=1)
        ad_btn = types.InlineKeyboardButton("🔓 Step 1: Unlock & Support", url=ADSTERRA_URL)
        check_btn = types.InlineKeyboardButton("✅ Step 2: Get Download Link", callback_data=f"get_link|{url}")
        markup.add(ad_btn, check_btn)
        bot.send_message(message.chat.id, "🚀 تمت معالجة الرابط!\n\n1️⃣ اضغط على الرابط الأول لدعمنا.\n2️⃣ اضغط على الزر الثاني للحصول على الفيديو.", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "يرجى إرسال رابط صحيح.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "جاري استخراج الرابط...")
    if "get_link|" in call.data:
        video_url = call.data.split("|")
        direct_link = generate_download_link(video_url)
        bot.send_message(call.message.chat.id, f"✅ تفضل، رابط التحميل جاهز:\n\n[📥 اضغط هنا للتحميل المباشر]({direct_link})", parse_mode="Markdown")

# تنظيف أي اتصال قديم وبدء العمل
bot.remove_webhook()
bot.polling(non_stop=True, skip_pending=True)
