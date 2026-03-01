import telebot
from telebot import types
import yt_dlp
import os
import http.server
import socketserver
import threading

# فتح منفذ وهمي لإرضاء Render
def start_server():
    port = 10000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=start_server, daemon=True).start()



# بيانات البوت الخاصة بك
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
    data = call.data.split("|")
    quality_choice = data
    video_url = data

    ad_markup = types.InlineKeyboardMarkup()
    ad_btn = types.InlineKeyboardButton("Click to Unlock & Download 🔓", url=ADSTERRA_URL)
    ad_markup.add(ad_btn)
    
    bot.edit_message_text(chat_id=call.message.chat.id, 
                         message_id=call.message.message_id, 
                         text="Processing... Click the link to support us and get your video:\nاضغط الرابط لفك التشفير واستلام الفيديو:", 
                         reply_markup=ad_markup)

    format_option = 'best' if quality_choice == "high" else 'worst'
    ydl_opts = {'format': format_option, 'outtmpl': f'video_{call.from_user.id}.mp4', 'quiet': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            filename = f'video_{call.from_user.id}.mp4'
            with open(filename, 'rb') as video:
                bot.send_video(call.message.chat.id, video, caption="Done! ✅")
            os.remove(filename)
    except Exception as e:
        bot.send_message(call.message.chat.id, "Error! Link might not be supported.")

bot.polling()
