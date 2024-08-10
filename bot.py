from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# Replace with your credentials
TELEGRAM_BOT_TOKEN = '6304912519:AAFS77ckUAENSMcKxxlibKNeUNTIKIAV-W4'
BLOGGER_API_KEY = 'AIzaSyAScLWfhhWU0KqeUlRaFtYaNy_yjITJUdI'
BLOG_ID = '215564800976830378'
BLOGGER_API_URL = f'https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send me a URL to shorten!')

async def shorten_url(update: Update, context: CallbackContext) -> None:
    url = ' '.join(context.args)
    if not url:
        await update.message.reply_text('Please send a URL to shorten.')
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
        # Note: Blogger API response may not contain 'url'. Adjust accordingly.
        shortened_url = response.json().get('url', 'URL shortening failed.')
        await update.message.reply_text(f'URL shortened: {shortened_url}')
    else:
        await update.message.reply_text('Failed to shorten URL.')

def main() -> None:
    # Initialize Application with the bot token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("shorten", shorten_url))

    application.run_polling()

if __name__ == '__main__':
    main()
