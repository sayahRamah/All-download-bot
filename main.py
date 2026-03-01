import telebot
from telebot import types
import yt_dlp

# بيانات البوت الخاصة بك
API_TOKEN = '8574425507:AAHLjTZ4W4xEQe5l9KLXYvbOfRbZhwkCukA'
ADSTERRA_URL = 'https://www.effectivegatecpm.com/tt2p09h6td?key=c8046088eb31ef124f0e28531e06bec0'

bot = telebot.TeleBot(API_TOKEN)

# دالة لاستخراج رابط التحميل المباشر فقط دون تحميل الملف
def get_direct_link(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('url', None)
    except:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Send me any video link to get the direct download link.\nأرسل رابط الفيديو للحصول على رابط التحميل المباشر:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        # إظهار زر الإعلان أولاً
        markup = types.InlineKeyboardMarkup()
        ad_btn = types.InlineKeyboardButton("🔓 Unlock Download Link (Step 1)", url=ADSTERRA_URL)
        # زر يضغط عليه المستخدم بعد رؤية الإعلان ليأخذ الرابط في تلغرام
        check_btn = types.InlineKeyboardButton("✅ I unlocked it, give me the link (Step 2)", callback_data=f"get|{url}")
        
        markup.add(ad_btn)
        markup.add(check_btn)
        
        bot.send_message(message.chat.id, 
                         "Your video is ready! Please complete these 2 steps:\nالفيديو جاهز! يرجى إتمام الخطوتين:\n\n"
                         "1️⃣ Click 'Unlock' to support us.\n"
                         "2️⃣ Click 'Get Link' to receive the direct download URL.", 
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Please send a valid link!")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("get|"):
        video_url = call.data.split("|")
        
        bot.answer_callback_query(call.id, "Generating link... please wait.")
        
        # استخراج الرابط المباشر
        direct_link = get_direct_link(video_url)
        
        if direct_link:
            msg_text = (f"✅ Here is your direct link:\nرابط التحميل المباشر الخاص بك:\n\n"
                        f"[Click here to Download / اضغط هنا للتحميل]({direct_link})\n\n"
                        f"Note: This link expires soon. Use it now!")
            bot.send_message(call.message.chat.id, msg_text, parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, "❌ Error: Could not extract link. Try another video.")

# تشغيل البوت
bot.polling(non_stop=True)
