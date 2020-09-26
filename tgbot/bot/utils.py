from tgbot.bot.constants import categories, max_categories
from tgbot.bot.texts import all_categories_text

def get_categories_keyboard(show_more_text, start = 0, end = max_categories):
  return [[all_categories_text, *categories[start:end], show_more_text]]
