from django.conf import settings

from telegram import Bot as TelegramBot, Update
from telegram.ext import Dispatcher, Updater

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from .models import Post, User


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CATEGORIES, CITIES = range(2)

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

    self.update_obj = None

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', self.start)],

        states={
          CITIES:     [MessageHandler(Filters.regex('^(Москва|Cпб)$'), self.cities)],
          CATEGORIES: [MessageHandler(Filters.regex('^(Все|Молоко|Хлеб)$'), self.categories)],
        },

        fallbacks=[CommandHandler('cancel', self.cancel)]
    )

    self.dispatcher.add_handler(conv_handler)


  def start(self, update, context):
    reply_keyboard = [['Москва', 'Спб']]

    self.update_obj.message.reply_text(
      'Привет! Это бот едудам. Поговори со мной. '
      'Отправь /cancel чтобы остановить разговор со мной.\n\n'
      'Выбери город',
      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CITIES

  def cities(self, update, context):
    user = self.update_obj.message.from_user
    reply_keyboard = [['Все', 'Молоко', 'Хлеб']]

    selected_city = self.update_obj.message.text
    user_db = User.objects.filter(user_id__exact=str(user.id)).get()
    user_db.update(
      city=selected_city
    )

    self.update_obj.message.reply_text(
      'Твой город: ' + selected_city + '\n\n'
      'Выбери интересующие категории продуктов ',
      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CATEGORIES


  def categories(self, update, context):
    self.update_obj.message.reply_text('Мы отфильтруем по выбранным категориям: ' + self.update_obj.message.text,
      reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

  def cancel(self, update, context):
    user = self.update_obj.message.from_user
    self.update_obj.message.reply_text('До встречи, ' + user.first_name,
      reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

  def register(self, handler):
    handler.register(self.dispatcher)

  def webhook(self, update):
    self.update_obj = Update.de_json(update, self.bot)
    self.dispatcher.process_update(self.update_obj)
