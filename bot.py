import os
import time
import requests
import snscrape.modules.twitter as sntwitter
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Lấy token & chat ID từ biến môi trường
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")

# Hàm gửi tin nhắn Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    if not response.ok:
        print("❌ Failed to send message:", response.text)

# Hàm lấy tweet mới nhất
def get_latest_tweet(username):
    tweets = sntwitter.TwitterUserScraper(username).get_items()
    for tweet in tweets:
        return tweet.content.strip()

# Vòng lặp kiểm tra tweet mới
if __name__ == "__main__":
    print("🚀 Bot đang chạy...")
    last_tweet = None
    while True:
        try:
            current_tweet = get_latest_tweet(TWITTER_USERNAME)
            if current_tweet and current_tweet != last_tweet:
                send_to_telegram(f"🆕 Bài mới từ @{TWITTER_USERNAME}:\n\n{current_tweet}")
                last_tweet = current_tweet
            else:
                print("⏳ Không có tweet mới.")
        except Exception as e:
            print("⚠️ Lỗi:", str(e))

        time.sleep(30)  # kiểm tra mỗi 30 giây
