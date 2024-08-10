from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from bs4 import BeautifulSoup
import requests

# Replace with your credentials and Blogger page URL
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
        # Fetch the Blogger page
        response = requests.get(BLOGGER_URL)
        response.raise_for_status()
        
        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the form action URL (assuming it's available)
        form_action = soup.find('form')['action']
        if not form_action:
            await update.message.reply_text('Form action URL not found.')
            return
        
        # Prepare form data
        form_data = {
            'url': url,  # Adjust this key according to the form field name
        }

        # Submit the form
        submit_response = requests.post(form_action, data=form_data)
        submit_response.raise_for_status()

        # Parse the response for the shortened URL
        submit_soup = BeautifulSoup(submit_response.text, 'html.parser')
        # Update this selector based on where the shortened URL is located
        shortened_url_tag = submit_soup.find('a', {'class': 'shortened-url-class'})
        
        if shortened_url_tag:
            shortened_url = shortened_url_tag['href']
            await update.message.reply_text(f'Shortened URL: {shortened_url}')
        else:
            await update.message.reply_text('Shortened URL not found in the response.')

    except requests.RequestException as e:
        await update.message.reply_text(f'HTTP Error: {e}')
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
