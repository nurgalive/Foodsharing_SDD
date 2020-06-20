from django.conf import settings

import logging

from telegram import Bot as TelegramBot, Update
from telegram.ext import Dispatcher, Updater

class Bot:
    def __init__(self, token, url):
      self.bot = TelegramBot(token)
      self.dispatcher = None

      # if settings.DEBUG:
      #     self.updater = Updater(token)
      #     self.dispatcher = self.updater.dispatcher

      #     self.updater.start_polling()
      # else:
      self.bot.set_webhook('{}/{}/{}/'.format(url, 'bot', token))

      self.dispatcher = Dispatcher(self.bot, None, workers=0)

    def register(self, handler):
      handler.register(self.dispatcher)

    def webhook(self, update):
      update_obj = Update.de_json(update, self.bot)
      self.dispatcher.process_update(update_obj)
      
      chat_id = str(update_obj.message.chat.id)

      text = update_obj.message.text
      self.bot.sendMessage(chat_id=chat_id, text=text)
