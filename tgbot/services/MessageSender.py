from tgbot.models import User, UserToCategory, Post
from datetime import datetime

from datetime import datetime

class MessageSender:
  def create(self, bot):
    users = User.objects.all()
    for user in users:

      user_db = User.objects.filter(user_id__exact=str(user.user_id)).get()
      user_categories = UserToCategory.objects.filter(user=user_db)
      categories = list(map(lambda qs: qs.category.name, user_categories))
      posts = Post.objects.filter(city__exact=user_db.city, is_book=False, is_lost=False)
      filtered_posts = []

      if 'Все' in categories:
        filtered_posts = posts
      else:
        for post in posts:
          if post.category in categories:
            filtered_posts.append(post)
      print(filtered_posts)

      if len(filtered_posts) == 0:
        continue

      for post in filtered_posts:
        info = ''
        if post.city is not None:
          info = info + '\nГород: ' + post.city + '\n'
        else:
          continue

        if post.category != 'unknown':
          info = info + 'Категория: ' + post.category + '\n'

        if post.metro != 'unknown':
          info = info + 'Метро: ' + post.metro + '\n'

        if post.address != 'Default address':
          info = info + 'Адрес: ' + post.address + '\n'

        info = info + '\n' + 'Ссылка на пост: ' + post.link + ''

      self.send_message(bot, user.user_id, info)
  
  def send_message(self, bot, chat_id, message):
    # Если пользователь заблокирован, выкидывает exception
    try:
      bot.send_message(chat_id=chat_id, text=message)
    except SendMessageError as error:
      print(error)
      print("Couldn't send message to user")