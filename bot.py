
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from key import apikey #get the key from key.py

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
        bot.sendMessage(update.message.chat_id, text='Welcome to dpastebot! Do /help for info')
        

def help(bot, update):
        bot.sendMessage(update.message.chat_id, text='Info coming soon')
        

def error(bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
        updater = Updater(apikey)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))

        #dp.add_handler(MessageHandler([Filters.text], echo))

        dp.add_error_handler(error)

        updater.start_polling()

        updater.idle()

if __name__ == '__main__':
        main()
