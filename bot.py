from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Replace with your credentials
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
BLOGGER_API_KEY = 'YOUR_BLOGGER_API_KEY'
BLOG_ID = 'YOUR_BLOG_ID'
BLOGGER_API_URL = f'https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a URL to shorten!')

def shorten_url(update: Update, context: CallbackContext) -> None:
    url = ' '.join(context.args)
    if not url:
        update.message.reply_text('Please send a URL to shorten.')
        return

    # Shorten URL using Blogger API
    response = requests.post(
        BLOGGER_API_URL,
        params={'key': BLOGGER_API_KEY},
        json={
            'title': 'Shortened URL',
            'content': f'<a href="{url}">{url}</a>'
        }
    )

    if response.status_code == 200:
        shortened_url = response.json().get('url')
        update.message.reply_text(f'URL shortened: {shortened_url}')
    else:
        update.message.reply_text('Failed to shorten URL.')

def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("shorten", shorten_url))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
