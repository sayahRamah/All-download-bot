import telebot
from telebot import types
import yt_dlp
import os
import http.server
import socketserver
import threading

# 1. فتح منفذ وهمي لإرضاء Render (لا تلمس هذا الجزء)
def start_server():
    port = 10000
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")

threading.Thread(target=start_server, daemon=True).start()

# 2. بيانات البوت الخاصة بك
API_TOKEN = '8574425507:AAHLjTZ4W4xEQe5l9KLXYvbOfRbZhwkCukA'
ADSTERRA_URL = 'https://www.effectivegatecpm.com/tt2p09h6td?key=c8046088eb31ef124f0e28531e06bec0'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Send me a link from (YouTube, TikTok, Instagram, FB) to download.\nأرسل رابط الفيديو للتحميل:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup()
        btn_high = types.InlineKeyboardButton("High Quality (HD) 🎬", callback_data=f"high|{url}")
        btn_low = types.InlineKeyboardButton("Low Quality (SD) 📱", callback_data=f"low|{url}")
        markup.add(btn_high, btn_low)
        bot.send_message(message.chat.id, "Select Video Quality / اختر الجودة:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Please send a valid link!")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # تصحيح استخراج البيانات
    try:
        data = call.data.split("|")
        quality_choice = data
        video_url = data
    except:
        bot.send_message(call.message.chat.id, "Data error!")
        return

    ad_markup = types.InlineKeyboardMarkup()
    ad_btn = types.InlineKeyboardButton("Click to Unlock & Download 🔓", url=ADSTERRA_URL)
    ad_markup.add(ad_btn)
    
    bot.edit_message_text(chat_id=call.message.chat.id, 
                         message_id=call.message.message_id, 
                         text="Processing... Click the link to support us and get your video:\nاضغط الرابط لفك التشفير واستلام الفيديو:", 
                         reply_markup=ad_markup)

    # إعدادات yt-dlp مع تحسينات التخفي
    format_option = 'best' if quality_choice == "high" else 'worst'
    filename = f'video_{call.from_user.id}.mp4'
    
    ydl_opts = {
        'format': format_option,
        'outtmpl': filename,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'add_header': [
            'Accept-Language: en-US,en;q=0.9',
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            
        if os.path.exists(filename):
            with open(filename, 'rb') as video:
                bot.send_video(call.message.chat.id, video, caption="Done! ✅")
            os.remove(filename)
        else:
            bot.send_message(call.message.chat.id, "Could not find the video file.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error: Link might be private or not supported.")

bot.polling(non_stop=True)
