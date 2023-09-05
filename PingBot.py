import logging
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = config.tk

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        fr"¡Hola, {user.mention_html()}!",
        reply_markup=None,
    )

def echo(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    if "ping" in message_text:
        update.message.reply_text("pong")
    elif re.match(r'^(\d+\s*,\s*)*\d+$', message_text):
        numbers = [int(num) for num in message_text.split(",")]
        result = sum(numbers)
        update.message.reply_text(f"El resultado es: {result}")
    else:
        update.message.reply_text("No entiendo ese comando.")

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.text & (Filters.regex(r'ping') | Filters.regex(r'^(\d+\s*,\s*)*\d+$')), echo))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
