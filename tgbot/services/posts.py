from tgbot.bot.texts import all_categories_text
from tgbot.models import User, UserToCategory, Post


def format_post(post):
  info = ''
  if post.city is not None:
    info = f'{info}\nГород: {post.city}\n'

  if post.category != 'unknown':
    info = f'{info}Категория: {post.category}\n'

  if post.metro != 'unknown':
    info = f'{info}Метро: {post.metro}\n'

  if post.address != 'Default address':
    info = f'{info}Адрес: {post.address}\n'

  info = f'{info}\nСсылка на пост: {post.link}\n'

  return info

def get_posts_for_user(user_id):
  user_db = User.objects.filter(user_id__exact=str(user_id)).get()
  user_categories = UserToCategory.objects.filter(user=user_db)

  categories = list(map(lambda qs: qs.category.name, user_categories))
  posts = Post.objects.filter(city__exact=user_db.city, is_book=False, is_lost=False)
  filtered_posts = []

  if all_categories_text in categories:
    return posts
  else:
    for post in posts:
      if post.category in categories:
        filtered_posts.append(post)

  return filtered_posts
