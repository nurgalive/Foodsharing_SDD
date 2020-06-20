from django.apps import AppConfig
from .bot import Bot

# class BotRegistry:
#     def __init__(self):
#         self.bots = {}

#     def add_bot(self, token, bot):
#         self.bots[token] = bot

#     def get_bot(self, token):
#         return self.bots.get(token)

class TgbotConfig(AppConfig):
    name = 'tgbot'
    registry = None

    def ready(self):
      Bot('1264768775:AAHvmoU7AZTvcL4ljxIDD78y048Rs5okQKU')