import base64
import json
import logging
import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackContext
)
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")


async def help(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "List of available commands:\n/help - Show this help message\n/start - Start the bot")


async def handle_image_request(update: Update, context: CallbackContext):
    file_obj = await update.message.photo[-1].get_file()
    img_response = requests.get(file_obj.file_path)
    url = 'http://host.docker.internal:5000/submit'
    if img_response.status_code == 200:
        img_bytes = img_response.content
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')  # Encode image data to base64 string
        payload = {'sample': img_base64}  # Prepare JSON payload
        response = requests.post(url, json=payload)  # Send JSON payload

        if response.status_code == 200:
            response = json.loads(response.text)
            label = response['label']
            probability = response['probability']
            message_content = f"The highest probability label is '{label}' with probability {probability:.2%}."
        else:
            message_content = "Error in processing image on server side"
    else:
        message_content = "Error in downloading image from Telegram"
    await update.message.reply_text(message_content)


def bot_start():
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image_request))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

