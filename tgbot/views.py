from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.decorators.csrf import csrf_exempt
# importing env variables
from django.conf import settings
# models
from .models import User, Message, Post, Group, Comment, Category, UserToCategory


import json
from datetime import datetime
import vk_api

from .apps import TgbotConfig
from .services.PostsFromVKCreator import PostsFromVKCreator
from .services.MessageAndUserFromWebhookJSON import MessageAndUserFromWebhookJSON

from .bot import Bot

from tgbot.machine_learning.get_category import all_cats

# To get value from env variable - settings.VK_LOGIN

def home(request):
  posts = Post.objects.all()
  return render(request, 'tgbot/home.html', {'posts' : posts})

# Уведомление пользователей c фильтрацией постов о новом посте в группе,
# на данный момент нет асинхронной задачи, но это сделано для наглядкости
def notify_users(request):

  #bot token
  token = settings.BOT_TOKEN
  bot = TgbotConfig.registry.get_bot(token)

  if bot is None:
    bot = Bot(token, url=settings.BOT_BASE_URL)
    TgbotConfig.registry.add_bot(token, bot)

  def send_message(self, chat_id, message):
    # Если пользователь заблокирован, выкидывает exception
    try:
      self.bot.send_message(chat_id=chat_id, text=message)
    except SendMessageError as error:
      print(error)
      print("Couldn't send message to user")

  users = User.objects.all()
  for user in users:

    user_db = User.objects.filter(user_id__exact=str(user.user_id)).get()
    user_categories = UserToCategory.objects.filter(user=user_db)
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

    send_message(bot, user.user_id, info)

  return redirect('home')

# Парсинг поста из ВК, морфологический разбор и ТП
def from_vk_to_db(request):
  login, password = settings.VK_LOGIN, settings.VK_PASS
  vk_session = vk_api.VkApi(login, password)
  try:
    vk_session.auth()
  except vk_api.AuthError as error_msg:
    print(error_msg)

  vk = vk_session.get_api()
  PostsFromVKCreator().create(vk)

  return redirect('home')

# Вебхук для обработка запросов от бота
@csrf_exempt
def webhook(request, token):
  bot = TgbotConfig.registry.get_bot(token)

  if bot is None:
    bot = Bot(token, url=settings.BOT_BASE_URL)
    TgbotConfig.registry.add_bot(token, bot)

  try:
    json_message = json.loads(request.body.decode('utf-8'))
  except json.decoder.JSONDecodeError as err:
    return HttpResponse(str(err))

  try:
    result = MessageAndUserFromWebhookJSON().save(json_message)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
  if result is True:
    if bot is not None:
      bot.webhook(json_message)
      return HttpResponse('OK')
    else:
      raise Http404

  else:
    return HttpResponseBadRequest('Malformed or incomplete JSON data received')

# Анализ постов и рендер страницы
def analytic(request):
  posts = Post.objects.all()
  category_stats = {}
  category_stats_arr = []

  for post in posts:
    if post.category in category_stats:
      category_stats[post.category] += 1
    else:
      category_stats[post.category] = 1

  for cat in category_stats:
    category_stats_arr.append({
      'cat': cat,
      'val': category_stats[cat]
    })

  post_from_moscow = Post.objects.filter(city__exact='Москва').count()
  post_from_spb = Post.objects.filter(city__exact='Санкт-Петербург').count()
  post_from_nowhere = Post.objects.filter(city__exact='Неизвестно').count()

  post_without_category = Post.objects.filter(category__exact='unknown').count()
  booked_postst = Post.objects.filter(is_book__exact=True).count()
  lost_posts = Post.objects.filter(is_lost__exact=True).count()

  return render(request, 'tgbot/analytic.html', {
    'category_stats': category_stats_arr,
    'post_from_moscow': post_from_moscow,
    'post_from_spb': post_from_spb,
    'post_from_nowhere': post_from_nowhere,
    'post_without_category': post_without_category,
    'booked_postst': booked_postst,
    'lost_posts': lost_posts,
    'all_posts': posts.count(),
  })

def upload_cats_to_db(request):
  for category in all_cats:
    if Category.objects.filter(name__exact=category).count() == 0:
      result = Category.objects.create(name=category)
      result.save()

  return redirect('home')
