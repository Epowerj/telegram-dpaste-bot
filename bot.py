
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, requests
from key import apikey #get the key from key.py

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
        bot.sendMessage(update.message.chat_id, text='Welcome to dpastebot! Do /help for info')
        

def help(bot, update):
        bot.sendMessage(update.message.chat_id, text='This bot is a front end for dpaste, an alternative to pastebin. Do /paste <text> and the bot will reply with a link.')


def paste(bot, update): #TODO add support for newline
        dpaste_url = 'http://dpaste.com/api/v2/'
        payload = {'content': update.message.text[7:], 'poster': update.message.from_user.first_name}
        r = requests.post(dpaste_url, data=payload)

        bot.sendMessage(update.message.chat_id, text= r.text)
        

def error(bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
        updater = Updater(apikey)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("paste", paste))

        #dp.add_handler(MessageHandler([Filters.text], echo))

        dp.add_error_handler(error)

        updater.start_polling()

        updater.idle()

if __name__ == '__main__':
        main()
