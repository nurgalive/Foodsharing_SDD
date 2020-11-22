from tgbot.models import User
from tgbot.services.posts import format_post, get_posts_for_user


class MessageSender:
  def create(self, bot):
    users = User.objects.all()
    for user in users:

      filtered_posts = get_posts_for_user(user.id)

      if len(filtered_posts) == 0:
        continue

      for post in filtered_posts:
        self.send_message(bot, user.user_id, format_post(post))


  
  def send_message(self, bot, chat_id, message):
    # Если пользователь заблокирован, выкидывает exception
    try:
      bot.send_message(chat_id=chat_id, text=message)
    except SendMessageError as error:
      print(error)
      print("Couldn't send message to user")