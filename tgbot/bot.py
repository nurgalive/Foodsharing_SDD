from django.conf import settings

import logging

from telegram import Bot as TelegramBot, Update
from telegram.ext import Dispatcher, Updater

update_id = None

def echo(bot):
  """Echo the message the user sent."""
  global update_id
  # Request updates after the last update_id
  for update in bot.get_updates(offset=update_id, timeout=10):
      update_id = update.update_id + 1

      if update.message:  # your bot can receive updates without messages
          # Reply to the message
          update.message.reply_text(update.message.text)



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

      global update_id

      # get the first pending update_id, this is so we can skip over it in case
      # we get an "Unauthorized" exception.
      try:
          update_id = self.bot.get_updates()[0].update_id
      except IndexError:
          update_id = None

      logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      
      echo(self.bot)

    def register(self, handler):
        handler.register(self.dispatcher)

    def webhook(self, update):
        self.dispatcher.process_update(Update.de_json(update, self.bot))