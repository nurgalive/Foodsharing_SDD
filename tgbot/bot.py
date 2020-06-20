from django.conf import settings

from telegram import Bot as TelegramBot, Update
from telegram.ext import Dispatcher, Updater, CallbackContext
from queue import Queue

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from utils.getCategory import all_cats
from .models import Post, User


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CATEGORIES, CITIES = range(2)

categories = list(all_cats.keys())
MAX_CATEGORIES = 5
show_more_text = 'Ещё'

class Bot:
  def __init__(self, token, url='edudam.herokuapp.com'):
    self.bot = TelegramBot(token)
    
    self.dispatcher = None

    self.bot.set_webhook('{}/{}/{}/'.format(url, 'bot', token))

    self.update_queue = Queue()
    self.dispatcher = Dispatcher(self.bot, self.update_queue, workers=4, use_context=True)

    self.update_obj = None

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
      entry_points=[CommandHandler('start', self.start)],

      states={
        CITIES:     [MessageHandler(Filters.regex('^(Москва|Санкт-Петербург)$'), self.cities)],
        CATEGORIES: [MessageHandler(Filters.regex(f'^(Все|{("|").join(categories)}|{show_more_text}_\d)$'), self.categories)],
      },

      fallbacks=[CommandHandler('cancel', self.cancel)]
    )

    self.dispatcher.add_handler(conv_handler)
    self.dispatcher.add_error_handler(self.error_handler)

  def error_handler(self, update: Update, context: CallbackContext):
    print('Error!', context.error)

  def start(self, update, context):
    reply_keyboard = [['Москва', 'Санкт-Петербург']]

    self.update_obj.message.reply_text(
      'Привет! Это бот едудам. Поговори со мной. '
      'Отправь /cancel чтобы остановить разговор со мной.\n\n'
      'Выбери город',
      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CITIES

  def cities(self, update, context):
    user = self.update_obj.message.from_user
    reply_keyboard = [['Все', *categories[:MAX_CATEGORIES], f'{show_more_text}_1']]

    selected_city = self.update_obj.message.text
    user_db = User.objects.filter(user_id__exact=str(user.id))

    if user_db is not None:
      user_db.update(
        city=selected_city
      )

    self.update_obj.message.reply_text(
      'Твой город: ' + selected_city + '\n\n'
      'Выбери интересующие категории продуктов ',
      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CATEGORIES


  def categories(self, update: Update, context: CallbackContext):
    category = self.update_obj.message.text

    if show_more_text in category:
      _, parsed_offset = category.split('_')
      offset = int(parsed_offset)
      start = offset * MAX_CATEGORIES
      end = offset * MAX_CATEGORIES + MAX_CATEGORIES

      reply_keyboard = [['Все', *categories[start:end], f'{show_more_text}_{offset+1}']]

      if len(categories) < end:
        reply_keyboard = [['Все', *categories[start:end]]]

      self.update_obj.message.reply_text(
        'Выбери интересующие категории продуктов ',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
      )

      return CATEGORIES

    self.update_obj.message.reply_text(
      'Мы отфильтруем по выбранным категориям: ' + category,
      reply_markup=ReplyKeyboardRemove())

    posts = Post.objects.all() 

    for post in posts:
      info = ''
      if post.city is not None:
        info = info + 'Город: ' + post.city + '\n'
      else:
        continue

      if post.metro is not 'unknown':
        info = info + 'Метро: ' + post.metro + '\n'

      if post.address is not None:
        info = info + 'Адрес: ' + post.address + '\n'

      self.update_obj.message.reply_text(
        '' + info + '\n\n'
        'Ссылка на пост: ' + post.link + ''
      )

    return ConversationHandler.END

  def cancel(self, update, context):
    user = self.update_obj.message.from_user
    self.update_obj.message.reply_text('До встречи, ' + user.first_name,
      reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

  def register(self, handler):
    handler.register(self.dispatcher)

  def webhook(self, update):
    self.update_queue.put(update)
    self.update_obj = Update.de_json(update, self.bot)
    self.dispatcher.process_update(self.update_obj)
