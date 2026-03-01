import telebot
from telebot import types
import urllib.parse
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

# 2. بيانات البوت
API_TOKEN = '8574425507:AAEAXECAtzC-MUJnAGnEBpUe_L-MnNRHUwg'
ADSTERRA_URL = 'https://www.effectivegatecpm.com/tt2p09h6td?key=c8046088eb31ef124f0e28531e06bec0'

bot = telebot.TeleBot(API_TOKEN)

# دالة توليد الرابط
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
    bot.reply_to(message, "✅ Bot is Online!\nأرسل رابط أي فيديو (TikTok, YT, IG) للتحميل المباشر:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup(row_width=1)
        # الزر الأول: الإعلان
        ad_btn = types.InlineKeyboardButton("🔓 Step 1: Unlock & Support", url=ADSTERRA_URL)
        # الزر الثاني: جلب الرابط (تأكد من الـ callback_data)
        check_btn = types.InlineKeyboardButton("✅ Step 2: Get Download Link", callback_data=f"get_link|{url}")
        
        markup.add(ad_btn, check_btn)
        
        bot.send_message(message.chat.id, 
                         "🚀 Video Link Processed!\n\n1️⃣ Click 'Step 1' (Ad).\n2️⃣ Click 'Step 2' to get the link.", 
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Please send a valid link!")

# معالج ضغطات الأزرار (Callback Query)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # إخبار تلغرام أننا استلمنا النقرة فوراً لإخفاء علامة التحميل على الزر
    bot.answer_callback_query(call.id, "Processing your request...")

    if "get_link|" in call.data:
        try:
            video_url = call.data.split("|")
            direct_link = generate_download_link(video_url)
            
            # إرسال النتيجة في رسالة جديدة لضمان الوضوح
            bot.send_message(call.message.chat.id, 
                             f"✅ **Success!**\n\n[📥 Click here to Download Video]({direct_link})\n\n"
                             f"*(If the page opens, just click the Download button)*", 
                             parse_mode="Markdown")
        except Exception as e:
            bot.send_message(call.message.chat.id, "❌ Error generating link. Please try again.")

# تشغيل البوت مع حذف الويب هوك وتجاهل الرسائل القديمة
bot.remove_webhook()
bot.polling(non_stop=True, skip_pending=True)
