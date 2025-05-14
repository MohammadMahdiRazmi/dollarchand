import requests
import telebot
import time
import threading

# ===== تنظیمات =====
API_KEY = 'Your API Key'  # کلید رایگان
TELEGRAM_BOT_TOKEN = 'TeleBot Token'  # توکن جدید ربات
CHAT_ID = 'Your chat ID'  # آیدی تلگرام شما

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

last_price = None

# دریافت قیمت دلار از API نواسان
def get_dollar_price():
    try:
        url = f'http://api.navasan.tech/latest/?api_key={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            price = int(data['usd']['value'])  # قیمت دلار
            return price
        else:
            print(f"❌ خطای دریافت قیمت: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ خطای ارتباط: {e}")
        return None

# نظارت بر تغییرات قیمت دلار
def monitor_price():
    global last_price
    while True:
        current_price = get_dollar_price()
        if current_price:
            print(f"💵 قیمت فعلی دلار: {current_price:,} تومان")
            if last_price is None:
                last_price = current_price
            elif current_price > last_price:
                bot.send_message(CHAT_ID, f'🔺 دلار شق کرد: {current_price:,} تومان')  # قیمت بالا رفت
                last_price = current_price
            elif current_price < last_price:
                bot.send_message(CHAT_ID, f'💤 دلار خوابید: {current_price:,} تومان')  # قیمت پایین آمد
                last_price = current_price
        else:
            print("❗ قیمت دریافت نشد.")
        time.sleep(100)  # هر 5 دقیقه

# فرمان /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! 👋\nمن ربات هشدار تغییر قیمت دلار هستم.\nهر وقت بالا یا پایین بره بهت خبر می‌دم!")

# فرمان /price برای دریافت قیمت لحظه‌ای دلار
@bot.message_handler(commands=['price'])
def send_price(message):
    price = get_dollar_price()
    if price:
        bot.reply_to(message, f"💵 قیمت لحظه‌ای دلار: {price:,} تومان")
    else:
        bot.reply_to(message, "❗ خطا در دریافت قیمت.")

# اجرای بررسی قیمت در بک‌گراند
threading.Thread(target=monitor_price).start()

# اجرای ربات
bot.infinity_polling()
