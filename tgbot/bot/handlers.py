from enum import Enum

class BotHandlersTypes(Enum):
  Help = 'help'
  Start = 'start'
  Cancel = 'cancel'
  ChooseCity = 'city'
  ChooseCategory = 'category'
  SetCity = 'set_city'
  SetCategory = 'set_category'
  Search = 'search'
  Dev = 'dev'


bot_handlers = [
  BotHandlersTypes.Help,
  BotHandlersTypes.Start,
  BotHandlersTypes.Cancel,
  BotHandlersTypes.ChooseCity,
  BotHandlersTypes.ChooseCategory,
  BotHandlersTypes.SetCity,
  BotHandlersTypes.SetCategory,
  BotHandlersTypes.Search,
  BotHandlersTypes.Dev,
]



class CallbackDatas(Enum):
  Dev = 'dev'

bot_callback_handlers = [
  CallbackDatas.Dev
]

