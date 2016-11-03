
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import logging, requests, os, urlparse2
from uuid import uuid4
from key import apikey #get the key from key.py

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
        bot.sendMessage(update.message.chat_id, text='Welcome to dpastebot! Do /help for info')


def help(bot, update):
        bot.sendMessage(update.message.chat_id, text='This bot is a front end for dpaste, an alternative to pastebin. Do /paste <text> and the bot will reply with a link.\nThis bot is currently running on an auto-sleep server, so it might take a while to respond for the first time')


def doPaste(content, user):
        print("Doing paste...")

        if content == "":
            return "(no text entered)"

        dpaste_url = 'http://dpaste.com/api/v2/'
        payload = {'content': content, 'poster': user}
        r = requests.post(dpaste_url, data=payload)

        return r.text


def paste(bot, update):
        commandtext = update.message.text.split(' ', 1)

        if len(commandtext) == 1:
            commandtext = ""
        else:
            commandtext = commandtext[1]

        link = doPaste(commandtext, update.message.from_user.first_name)

        bot.sendMessage(update.message.chat_id, text= link)


def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Get link",
                                            input_message_content=InputTextMessageContent(
                                                doPaste(query, update.inline_query.from_user.first_name)
                                            )))

    update.inline_query.answer(results)


def error(bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
        TOKEN = apikey
        PORT = int(os.environ.get('PORT', '5000'))
        updater = Updater(TOKEN)
        dp = updater.dispatcher
        # add handlers
        updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
        updater.bot.setWebhook("https://" + str(os.environ.get("APPNAME")) + ".herokuapp.com/" + TOKEN)

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("paste", paste))

        #dp.add_handler(InlineQueryHandler(inlinequery))

        #dp.add_handler(MessageHandler([Filters.text], echo))

        dp.add_error_handler(error)

        updater.idle()

if __name__ == '__main__':
        main()
