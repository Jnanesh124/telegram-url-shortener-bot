from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from bs4 import BeautifulSoup
import requests

# Replace with your credentials and API details
TELEGRAM_BOT_TOKEN = '6304912519:AAFS77ckUAENSMcKxxlibKNeUNTIKIAV-W4'
BLOGGER_URL = 'https://rockers-disc-link.blogspot.com/p/safelink-generator.html'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send me a URL to shorten!')

async def shorten_url(update: Update, context: CallbackContext) -> None:
    url = ' '.join(context.args)
    if not url:
        await update.message.reply_text('Please send a URL to shorten.')
        return

    try:
        # Use BeautifulSoup to scrape the Blogger page
        response = requests.get(BLOGGER_URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Assuming the form action URL and parameters are needed for submission
        # You will need to update this with the correct form parameters and URLs
        form_action = soup.find('form')['action']
        form_data = {
            'url': url,  # Adjust the form data key based on actual form fields
        }

        # Submit the URL to the Blogger page
        submit_response = requests.post(form_action, data=form_data)
        submit_soup = BeautifulSoup(submit_response.text, 'html.parser')

        # Extract the shortened URL from the response
        # You need to update this based on where the shortened URL is located
        shortened_url = submit_soup.find('a', {'class': 'shortened-url-class'})['href']
        await update.message.reply_text(f'Shortened URL: {shortened_url}')

    except Exception as e:
        await update.message.reply_text(f'Error: {e}')

def main() -> None:
    # Initialize Application with the bot token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("shorten", shorten_url))

    application.run_polling()

if __name__ == '__main__':
    main()
