import logging

from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher, CallbackContext
from utils import get_reply, fetch_news

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# telegram bot token (not to be displayed to everyone )
TOKEN = "5041958555:AAHKlirsEo8SmP8k4x8R6sbG7mJI0Z5tgw4"

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello!"


@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    """webhook view which receives updates from telegram"""
    # create update object from json-format request data
    update = Update.de_json(request.get_json(), bot)
    # process update
    dp.process_update(update)
    return "ok"


def start(update, bot):
    """callback function for /start handler"""
    author = update.message.from_user.first_name
    reply = "Hi! {}".format(author)
    bot.send_message(chat_id=update.message.chat_id, text=reply)


def _help(update, bot):
    """callback function for /help handler"""
    help_txt = "Hey! This is a help text."
    bot.send_message(chat_id=update.message.chat_id, text=help_txt)


def reply_text(update, bot):
    """callback function for text message handler"""
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            bot.send_message(chat_id=update.message.chat_id, text=article['link'])
    else:
        bot.send_message(chat_id=update.message.chat_id, text=reply)


def echo_sticker(update, bot):
    """callback function for sticker message handler"""
    bot.send_sticker(chat_id=update.message.chat_id,
                     sticker=update.message.sticker.file_id)


def error(update, bot):
    """callback function for error handler"""
    logger.error("Update '%s' caused error '%s'", bot, bot.error)


if __name__ == "__main__":
    bot = Bot(TOKEN)

    # Setting a webhook server
    bot.set_webhook("https://3c3a-2405-201-3012-201a-5cde-2d02-416d-adda.ngrok.io/" + TOKEN)

    dp = Dispatcher(bot, None)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(MessageHandler(Filters.text, reply_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    dp.add_error_handler(error)

    app.run(port=8443)