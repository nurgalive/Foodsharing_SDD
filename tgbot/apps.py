from django.apps import AppConfig

class BotRegistry:
    def __init__(self):
        self.bots = {}

    def add_bot(self, token, bot):
        self.bots[token] = bot

    def get_bot(self, token):
        return self.bots.get(token)

class TgbotConfig(AppConfig):
    name = 'tgbot'
    registry = None

    def ready(self):
        TgbotConfig.registry = BotRegistry()