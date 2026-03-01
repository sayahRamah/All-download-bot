import telebot
from telebot import types
import urllib.parse

# بيانات البوت
API_TOKEN = '8574425507:AAFlgLekwiUQtVqRWZZSOtH8MGyt9wJlRz4'
ADSTERRA_URL = 'https://www.effectivegatecpm.com/tt2p09h6td?key=c8046088eb31ef124f0e28531e06bec0'

bot = telebot.TeleBot(API_TOKEN)

def generate_download_link(url):
    # ترميز الرابط ليكون صالحاً للاستخدام في المتصفح
    encoded_url = urllib.parse.quote(url)
    
    if "tiktok.com" in url:
        return f"https://snaptik.app/abc.php?url={encoded_url}"
    elif "youtube.com" in url or "youtu.be" in url:
        return f"https://en.savefrom.net/1-youtube-video-downloader-521/v7/?url={encoded_url}"
    elif "instagram.com" in url:
        return f"https://snapinst.app/en/instagram-reels-download?url={encoded_url}"
    else:
        # رابط عام يدعم أغلب المواقع
        return f"https://en.savefrom.net/results?url={encoded_url}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Bot is Ready! Send me any video link.\nأرسل رابط أي فيديو للتحميل المباشر:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        markup = types.InlineKeyboardMarkup()
        # الخطوة 1: رابط أدستيرا للربح
        ad_btn = types.InlineKeyboardButton("🔓 Step 1: Unlock & Support", url=ADSTERRA_URL)
        # الخطوة 2: الحصول على الرابط الفعلي
        check_btn = types.InlineKeyboardButton("✅ Step 2: Get Download Link", callback_data=f"get|{url}")
        
        markup.add(ad_btn)
        markup.add(check_btn)
        
        bot.send_message(message.chat.id, 
                         "🚀 Your video link is processed!\n\n1️⃣ Click 'Step 1' to support us.\n2️⃣ Click 'Step 2' to get the direct download link.", 
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Please send a valid link!")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("get|"):
        video_url = call.data.split("|")
        direct_link = generate_download_link(video_url)
        
        # إرسال الرابط للمستخدم مباشرة
        bot.send_message(call.message.chat.id, 
                         f"✅ **Success!**\n\n[📥 Click here to Download Video]({direct_link})\n\n"
                         f"*(If the page opens, just click the Download button)*", 
                         parse_mode="Markdown")

bot.polling(non_stop=True, skip_pending=True)
