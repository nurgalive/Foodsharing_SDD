from telegram import Bot as TelegramBot, ReplyKeyboardRemove, ReplyKeyboardMarkup, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler
from queue import Queue

from tgbot.bot.constants import categories, max_categories
from tgbot.bot.utils import get_categories_keyboard
from tgbot.bot.handlers import BotHandlersTypes, bot_handlers
from tgbot.bot.texts import BotTextsTypes, bot_texts, show_more_text, cities
from tgbot.services.user import update_user_city
from .models import Post, User, Category, UserToCategory


# Основной класс для бота для телеграма
class Bot:
  def __init__(self, token, url):
    self.bot = TelegramBot(token)

    self.bot.set_webhook(f'{url}/bot/{token}/')

    self.update_queue = Queue()
    self.dispatcher = Dispatcher(self.bot, self.update_queue, workers=4, use_context=True)
    self.update_obj = None

    self.__register_handlers__()

  def __register_handlers__(self):
    handlers = self.__get_handlers__()

    for command in bot_handlers:
      self.dispatcher.add_handler(
        handlers[command]['handler_type'](handlers[command]['command'], handlers[command]['callback'])
      )

  def __get_handlers__(self):
    return {
      BotHandlersTypes.Help: {
        'command': 'help',
        'handler_type': CommandHandler,
        'callback': self.help,
      },
      BotHandlersTypes.Start: {
        'command': 'start',
        'handler_type': CommandHandler,
        'callback': self.start,
      },
      BotHandlersTypes.Cancel: {
        'command': 'cancel',
        'handler_type': CommandHandler,
        'callback': self.cancel,
      },
      BotHandlersTypes.ChooseCity: {
        'command': 'city',
        'handler_type': CommandHandler,
        'callback': self.choose_city,
      },
      BotHandlersTypes.ChooseCategory: {
        'command': 'category',
        'handler_type': CommandHandler,
        'callback': self.choose_category,
      },
      BotHandlersTypes.SetCity: {
        'command': Filters.regex(f'^({"|".join(cities)})$'),
        'handler_type': MessageHandler,
        'callback': self.set_cities,
      },
      BotHandlersTypes.SetCategory: {
        'command': Filters.regex(f'^(Все|{("|").join(categories)}|{show_more_text}_\d)$'),
        'handler_type': MessageHandler,
        'callback': self.set_category,
      },
      BotHandlersTypes.Search: {
        'command': 'search',
        'handler_type': CommandHandler,
        'callback': self.search,
      }
    }

  def __get_user_field__(self, field_name = None):
    if field_name is not None:
      return self.update_obj.message.from_user[field_name]

    return self.update_obj.message.from_user

  def error_handler(self, _update, context):
    print('Error!', context.error)

  def start(self, update, context):
    self.update_obj.message.reply_text(bot_texts[BotTextsTypes.Start])

  def help(self, update, context):
    self.update_obj.message.reply_text(bot_texts[BotTextsTypes.Help])

  def choose_city(self, update, context):
    self.update_obj.message.reply_text(
      bot_texts[BotTextsTypes.ChooseCity],
      reply_markup=ReplyKeyboardMarkup([cities], one_time_keyboard=True)
    )

  def choose_category(self, update, context):
    print('test')
    reply_keyboard = get_categories_keyboard(show_more_text, end=max_categories)

    self.update_obj.message.reply_text(
      bot_texts[BotTextsTypes.ChooseCategory],
      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

  def set_cities(self, update, context):
    user_id = self.__get_user_field__('id')
    selected_city = self.update_obj.message.text

    update_user_city(user_id, selected_city)

    self.update_obj.message.reply_text(f'Твой город: {selected_city}\n\n')

  def cancel(self, update, context):
    user_first_name = self.__get_user_field__('first_name')

    self.update_obj.message.reply_text(
      f'До встречи, {user_first_name}',
      reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

  def set_category(self, update, context):
    category = self.update_obj.message.text

    if show_more_text in category:
      _, parsed_offset = category.split('_')
      offset = int(parsed_offset)
      start = offset * max_categories
      end = offset * max_categories + max_categories

      reply_keyboard = [['Все', *categories[start:end], f'{show_more_text}_{offset + 1}']]

      if len(categories) < end:
        reply_keyboard = [['Все', *categories[start:end]]]

      self.update_obj.message.reply_text(
        'Выбери интересующие категории продуктов ',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
      )

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
        f'Категория "{category}" уже добавлена',
        reply_markup=ReplyKeyboardRemove()
      )

  def search(self, update, context):
    user = self.update_obj.message.from_user
    user_db = User.objects.filter(user_id__exact=str(user.id)).get()
    user_categories = UserToCategory.objects.filter(user=user_db)

    categories = list(map(lambda qs: qs.category.name, user_categories))
    posts = Post.objects.filter(city__exact=user_db.city, is_book=False, is_lost=False)
    filtered_posts = []

    if 'Все' in categories:
      filtered_posts = posts
    else:
      for post in posts:
        if post.category in categories:
          filtered_posts.append(post)

    if len(filtered_posts) == 0:
      self.update_obj.message.reply_text('Ни одного поста не найдено')

      return ConversationHandler.END

    for post in filtered_posts:
      info = ''
      if post.city is not None:
        info = info + '\nГород: ' + post.city + '\n'
      else:
        continue

      if post.category != 'unknown':
        info = info + 'Категория: ' + post.category + '\n'

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
