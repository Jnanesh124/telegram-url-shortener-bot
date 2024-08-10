from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# Replace with your credentials
TELEGRAM_BOT_TOKEN = '6304912519:AAFS77ckUAENSMcKxxlibKNeUNTIKIAV-W4'
SHORTENING_SERVICE_API_URL = 'https://api.your-url-shortening-service.com/shorten'
API_KEY = 'AIzaSyAScLWfhhWU0KqeUlRaFtYaNy_yjITJUdI'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send me a URL to shorten!')

async def shorten_url(update: Update, context: CallbackContext) -> None:
    url = ' '.join(context.args)
    if not url:
        await update.message.reply_text('Please send a URL to shorten.')
        return

    # Shorten URL using an external URL shortening service
    response = requests.post(
        SHORTENING_SERVICE_API_URL,
        json={
            'url': url,
            'api_key': API_KEY
        }
    )

    if response.status_code == 200:
        data = response.json()
        shortened_url = data.get('shortened_url', 'URL shortening failed.')
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
