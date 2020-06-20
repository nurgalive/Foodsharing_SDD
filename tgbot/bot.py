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

LOCATION, BIO = range(2)


def start(update, context):
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return LOCATION


def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(update, context):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    posts = Post.objects.all()
    for post in posts:
        update.message.reply_text(post.text)
    

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

      self.dispatcher.process_update(update_obj)

      # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
      conv_handler = ConversationHandler(
          entry_points=[CommandHandler('start', start(update_obj, self.bot))],

          states={
              LOCATION: [MessageHandler(Filters.location, location(update_obj, self.bot)),
                        CommandHandler('skip', skip_location(update_obj, self.bot))],
              BIO: [MessageHandler(Filters.text, bio(update_obj, self.bot))]
          },

          fallbacks=[CommandHandler('cancel', cancel(update_obj, self.bot))]
      )

    self.dispatcher.add_handler(conv_handler)