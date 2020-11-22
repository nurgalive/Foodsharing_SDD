from tgbot.bot.constants import categories, max_categories
from tgbot.bot.texts import all_categories_text, show_more_text

def get_categories_keyboard(show_more_text, start = 0, end = max_categories):
  if len(categories) < end:
    return [[all_categories_text, *categories[start:end]]]
  else:
    return [[all_categories_text, *categories[start:end], show_more_text]]

def get_more_categories_keyboard(offset):
  start = offset * max_categories
  end = start + max_categories

  return get_categories_keyboard(f'{show_more_text}_{offset + 1}', start, end)
