from enum import Enum

class BotTextsTypes(Enum):
  Help = 'help'
  Start = 'start'
  Cancel = 'cancel'
  ChooseCity = 'city'
  ChooseCategory = 'category'
  SetCity = 'set_city'
  SetCategory = 'set_category'
  Search = 'search'

bot_texts = {
  BotTextsTypes.Start: '''Привет! Это бот едудам. Я могу тебе помочь!
Отправь /cancel чтобы остановить разговор со мной.
Отправь /help чтобы узнать что я умею.''',
  BotTextsTypes.Help: '''Привет! Это бот едудам. Я могу тебе помочь!
Отправь /cancel чтобы остановить разговор со мной.
Отправь /city чтобы выбрать город.
Отправь /category чтобы выбрать категорию.
Отправь /search чтобы искать объявления.''',
  BotTextsTypes.ChooseCity: 'Выбери город',
  BotTextsTypes.ChooseCategory: 'Выбери категорию',
}

all_categories_text = 'Все'
show_more_text = 'Ещё'
cities = ['Москва', 'Санкт-Петербург']
