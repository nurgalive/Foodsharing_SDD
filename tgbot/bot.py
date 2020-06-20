from django.conf import settings

from telegram import Bot as TelegramBot, Update
from telegram.ext import Dispatcher, Updater

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from .models import Post


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CATEGORIES = range(1)


def start(update, context):
  reply_keyboard = [['Москва', 'Спб']]

  update.message.reply_text(
    'Привет! Это бот едудам. Поговори со мной. '
    'Отправь /cancel чтобы остановить разговор со мной.\n\n'
    'Выбери город',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

  return LOCATION


def categories(update, context):
  reply_keyboard = [['Все', 'Молоко', "Хлеб"]]
  user = update.message.from_user

  update.message.reply_text(
    'Выбери интересующие категории продуктов',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

  return ConversationHandler.END


def cancel(update, context):
  user = update.message.from_user
  logger.info("User %s canceled the conversation.", user.first_name)
  update.message.reply_text('Bye! I hope we can talk again some day.',
                            reply_markup=ReplyKeyboardRemove())

  return ConversationHandler.END

class Bot:
  def __init__(self, token, url='edudam.herokuapp.com'):
    self.bot = TelegramBot(token)
    
    self.dispatcher = None

    # if settings.DEBUG:
    # self.updater = Updater(token)
    # self.dispatcher = self.updater.dispatcher
        
    # else:
    self.bot.set_webhook('{}/{}/{}/'.format(url, 'bot', token))

    self.dispatcher = Dispatcher(self.bot, None, workers=0)
    

  def register(self, handler):
    handler.register(self.dispatcher)

  def webhook(self, update):
    update_obj = Update.de_json(update, self.bot)

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start(update_obj, self.bot))],

        states={
          CATEGORIES: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), categories(update_obj, self.bot))],
        },

        fallbacks=[CommandHandler('cancel', cancel(update_obj, self.bot))]
    )

    self.dispatcher.add_handler(conv_handler)
    self.dispatcher.process_update(update_obj)
