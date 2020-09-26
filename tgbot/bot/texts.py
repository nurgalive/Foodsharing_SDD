from enum import Enum

class BotTextsTypes(Enum):
  Help = 'help'
  Start = 'start'
  Cancel = 'cancel'
  ChooseCity = 'city'
  ChooseCategory = 'category'
  SetCity = 'set_ity'
  SetCategory = 'set_category'
  Search = 'search'

bot_texts = {
  [BotTextsTypes.Start]: '''Привет! Это бот едудам. Поговори со мной.
      Отправь /cancel чтобы остановить разговор со мной.\n
      Отправь /help чтобы узнать что я умею.\n''',
  [BotTextsTypes.Help]: '''Привет! Это бот едудам. Поговори со мной.
      Отправь /cancel чтобы остановить разговор со мной.\n
      Отправь /city чтобы выбрать город.\n
      Отправь /category чтобы выбрать категорию.\n
      Отправь /search чтобы искать объявления.\n''',
  [BotTextsTypes.ChooseCity]: 'Выбери город',
  [BotTextsTypes.SetCategory]: 'Выбери категорию',
}

all_categories_text = 'Все'
show_more_text = 'Ещё'
cities = ['Москва', 'Санкт-Петербург']
