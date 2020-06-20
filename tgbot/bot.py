from django.conf import settings

from telegram import Bot as TelegramBot, Update
from telegram.ext import Dispatcher, Updater, CallbackContext
from queue import Queue

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from utils.getCategory import all_cats
from .models import Post, User, Category, UserToCategory


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

    # Хендлер регистрации с состояниями CITIES and CATEGORIES
    register_handler = ConversationHandler(
      entry_points=[CommandHandler('start', self.start)],

      states={
        CITIES:     [MessageHandler(Filters.regex('^(Москва|Санкт-Петербург)$'), self.cities)],
        CATEGORIES: [MessageHandler(Filters.regex(f'^(Все|{("|").join(categories)}|{show_more_text}_\d)$'), self.categories)],
      },

      fallbacks=[CommandHandler('cancel', self.cancel)]
    )

    # Хендлер поиска
    search_handler = ConversationHandler(
      entry_points=[CommandHandler('search', self.search)],
      states={},
      fallbacks=[CommandHandler('cancel', self.cancel)]
    )

    self.dispatcher.add_handler(register_handler)
    self.dispatcher.add_handler(search_handler)
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

    user = self.update_obj.message.from_user
    user_db = User.objects.filter(user_id__exact=str(user.id)).get()
    category_db = Category.objects.filter(name__exact=str(category)).get()
    user_categories = UserToCategory.objects.filter(user=user_db, category=category_db)
    
    try:
      if user_categories.count() == 0:
        UserToCategory(
          user=user_db,
          category=category_db
        ).save()
    except (KeyError, ValueError):
      return self.update_obj.message.reply_text('Ошибка при добавлении категории')

    if user_categories.count() == 0:
      self.update_obj.message.reply_text(
        'Мы отфильтруем по выбранным категориям: ' + category,
        reply_markup=ReplyKeyboardRemove()
      )
    else:
      self.update_obj.message.reply_text(
        f'Категоря "{category}" уже добавлена',
        reply_markup=ReplyKeyboardRemove()
      )



    return ConversationHandler.END

  def cancel(self, update, context):
    user = self.update_obj.message.from_user
    self.update_obj.message.reply_text('До встречи, ' + user.first_name,
      reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

  def search(self, update, context):
    user = self.update_obj.message.from_user
    user_db = User.objects.filter(user_id__exact=str(user.id)).get()
    user_categories = UserToCategory.objects.filter(user=user_db)
    #categories_db = Category.objects.filter(id=user_categories.category)
    for qs in user_categories:
      print(qs.category.name)

    categories = map(lambda qs: qs.category.name, user_categories)

    posts = []
    if 'Все' in categories:
      posts.append(Post.objects.filter(city__exact=user_db.city))
    else:
      posts.append(Post.objects.filter(city__exact=user_db.city, category__exact=categories))

    for post in posts[:5]:
      info = ''
      if post.city is not None:
        info = info + '\nГород: ' + post.city + '\n'
      else:
        continue

      if post.metro != 'unknown':
        info = info + 'Метро: ' + post.metro + '\n'

      if post.address != 'Default address':
        info = info + 'Адрес: ' + post.address + '\n'

      self.update_obj.message.reply_text(
        '' + info + '\n'
                    'Ссылка на пост: ' + post.link + ''
      )

    return ConversationHandler.END

  def register(self, handler):
    handler.register(self.dispatcher)

  def webhook(self, update):
    self.update_queue.put(update)
    self.update_obj = Update.de_json(update, self.bot)
    self.dispatcher.process_update(self.update_obj)
