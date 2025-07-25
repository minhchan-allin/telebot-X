import snscrape.modules.twitter as sntwitter
import asyncio
from telegram import Bot

TELEGRAM_BOT_TOKEN = '8340498820:AAHunbMFycOrOtL7Ov5a81mmOROa8xoLgeQ'
TELEGRAM_CHAT_ID = -4884617653  # thay bằng chat_id nhóm của bạn (số âm nếu là private group)
RSS_FEED_URL = 'grutgrutx'

bot = Bot(token=TELEGRAM_BOT_TOKEN)
last_tweet_id = None

async def check_tweet():
    global last_tweet_id
    tweets = sntwitter.TwitterUserScraper(TWITTER_USERNAME).get_items()
    for tweet in tweets:
        if tweet.id != last_tweet_id:
            last_tweet_id = tweet.id
            message = f"🆕 New tweet by @{TWITTER_USERNAME}:\n\n{tweet.content}\n\n🔗 https://twitter.com/{TWITTER_USERNAME}/status/{tweet.id}"
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        break

async def main():
    while True:
        try:
            await check_tweet()
        except Exception as e:
            print(f"❌ Error: {e}")
        await asyncio.sleep(30)  # vẫn phải kiểm tra định kỳ

if __name__ == '__main__':
    asyncio.run(main())