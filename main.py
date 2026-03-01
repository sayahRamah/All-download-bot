import telebot
from telebot import types
import yt_dlp
import os
import http.server
import socketserver
import threading

# 1. فتح منفذ وهمي لإرضاء Render ومنع إغلاق البوت
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

# دالة استخراج الرابط المباشر (بدون تحميل الفيديو على السيرفر)
def get_direct_link(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('url', None)
    except:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Send me any video link (TikTok, YT, IG) to get the direct download link.\nأرسل رابط الفيديو للحصول على رابط التحميل المباشر:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup()
        # الخطوة 1: رابط أدستيرا
        ad_btn = types.InlineKeyboardButton("🔓 Unlock Download Link (Step 1)", url=ADSTERRA_URL)
        # الخطوة 2: زر الحصول على الرابط داخل تلغرام
        check_btn = types.InlineKeyboardButton("✅ Get Direct Link (Step 2)", callback_data=f"get|{url}")
        
        markup.add(ad_btn)
        markup.add(check_btn)
        
        bot.send_message(message.chat.id, 
                         "🚀 Your video is ready!\n\n1️⃣ Click 'Unlock' to support us (Open Ad).\n2️⃣ Click 'Get Direct Link' to receive the URL.", 
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Please send a valid link!")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("get|"):
        video_url = call.data.split("|")
        bot.answer_callback_query(call.id, "Extracting link... Please wait.")
        
        direct_link = get_direct_link(video_url)
        
        if direct_link:
            # إرسال الرابط المباشر للمستخدم
            response = (f"✅ **Link Extracted!**\n\n[Click here to Download / اضغط للتحميل]({direct_link})\n\n"
                       f"💡 *Tip: Long press the link/video and select 'Save' to download to your gallery.*")
            bot.send_message(call.message.chat.id, response, parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, "❌ Sorry, could not extract link from this URL. Try another one.")

# تشغيل البوت مع تخطي الرسائل القديمة المتراكمة
bot.polling(non_stop=True, skip_pending=True)
