from enum import Enum

class BotHandlersTypes(Enum):
  Help = 'help'
  Start = 'start'
  Cancel = 'cancel'
  ChooseCity = 'city'
  ChooseCategory = 'category'
  SetCity = 'set_ity'
  SetCategory = 'set_category'
  Search = 'search'


bot_handlers = [
  BotHandlersTypes.Help,
  BotHandlersTypes.Start,
  BotHandlersTypes.Cancel,
  BotHandlersTypes.ChooseCity,
  BotHandlersTypes.ChooseCategory,
  BotHandlersTypes.SetCity,
  BotHandlersTypes.SetCategory,
  BotHandlersTypes.Search,
]
