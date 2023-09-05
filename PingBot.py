import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = "6580788874:AAEiJlmTDuiV2XBObehQHK6X-2U1iCMNRxU"

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        fr"¡Hola, {user.mention_html()}!",
        reply_markup=None,
    )

def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("pong")

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.regex(r'ping'), echo))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
