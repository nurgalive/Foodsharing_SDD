from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.decorators.csrf import csrf_exempt
import json

from utils.getCategory import get_food_category, all_cats
from utils.gitCity import get_city, get_metro_station
from utils.getIsBooked import get_is_booked
from utils.getIsLost import get_is_lost
from .models import User, Message, Post, Group, Comment, Category, UserToCategory
from datetime import datetime
import vk_api

from .apps import TgbotConfig
from .services import MessageAndUserFromWebhookJSON
from .bot import Bot

def home(request):
  posts = Post.objects.all()
  return render(request, 'tgbot/home.html', {'posts' : posts})

def notify_users(request):
  token = "1264768775:AAHvmoU7AZTvcL4ljxIDD78y048Rs5okQKU"
  bot = TgbotConfig.registry.get_bot(token)
  
  if bot is None:
    bot = Bot(token)
    TgbotConfig.registry.add_bot(token, bot)

    #print(self.bot.send_message(chat_id=42737369, text="Хэй, бро!"))

  #message = "Хэй, бро!"
  def send_message(self, chat_id, message):
    self.bot.send_message(chat_id=chat_id, text=message)
    #self.bot.send_message(chat_id=42737369, text=message)
    #self.bot.send_message(chat_id=217254731, text=message)

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
        info =  info + '\n' + 'Ссылка на пост: ' + post.link + ''


    send_message(bot, user.user_id, info)

  #bot.send_message(chat_id=42737369, text="Хэй, бро!")
  #bot.send_message(chat_id=217254731, text="Хэй, бро!")

  return redirect('home')


def from_vk_to_db(request):
  login, password = '+4915205901185', '78ododad'
  vk_session = vk_api.VkApi(login, password)
  try:
    vk_session.auth()
  except vk_api.AuthError as error_msg:
    print(error_msg)

  vk = vk_session.get_api()

  groups = Group.objects.all()
  for group in groups:
    domain = group.link[15:len(group.link)]
    for x in range(0,5):
      post = vk.wall.get(domain=domain, count=5)
      text = post['items'][x]['text']
      date = post['items'][x]['date']
      post_id = post['items'][x]['id']
      group_id = post['items'][x]['owner_id']
      city = get_city(text)
      is_book = get_is_booked(text)
      category = get_food_category(text)
      is_lost = get_is_lost(text)
      metro = get_metro_station(text)

      #print(post_id)

      #       try:
      #   Post.objects.filter(post_id=post_id)
      # except:

      if Post.objects.filter(post_id = post_id).exists():
        continue
      else:
        group_id = group_id * -1
        group = Group.objects.get(group_id=group_id)

        group_id = group_id * -1
        comments = vk.wall.getComments(owner_id=group_id, post_id=post_id, count=100, sort='asc')

        count = comments['current_level_count']
        big_comment = ""
        for x in range(0,count):
          try:
            comments['items'][x]['deleted'] == True
            continue
          except:
            try:
             comment_text = comments['items'][x]['text']
             big_comment = big_comment + comment_text + " "
            except IndexError:
              continue

            #print(text)
              

        # last comment id
        #last_comment_id = comments['items'][count-1]['id']
        # resulted comment
        #print(big_comment)
        is_book_from_comment = get_is_booked(big_comment)
        is_lost_from_comment = get_is_lost(big_comment)

        result = Post.objects.create(
          post_id=post_id,
          text=text,
          posted_date=datetime.fromtimestamp(int(date)),
          link="https://vk.com/"+domain+"?w=wall"+str(group_id)+"_"+str(post_id),
          group_id=group,
          city=city.value,
          address="Default address",
          is_book=is_book | is_book_from_comment,
          category=category,
          is_lost=is_lost | is_lost_from_comment,
          metro=metro
        )
        result.save()

  return redirect('home')

def upload_cats_to_db(request):
  for category in all_cats:
    if Category.objects.filter(name__exact=category).count() == 0:
      result = Category.objects.create(name=category)
      result.save()

  return redirect('home')

@csrf_exempt
def webhook(request, token):
  bot = TgbotConfig.registry.get_bot(token)
  
  if bot is None:
    bot = Bot(token)
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

  post_without_category = Post.objects.filter(category__exact='unknow').count()
  booked_postst = Post.objects.filter(category__exact='unknow').count()
  lost_posts = Post.objects.filter(category__exact='unknow').count()

  return render(request, 'tgbot/analytic.html', {
    'category_stats': category_stats_arr,
    'post_from_moscow': post_from_moscow,
    'post_from_spb': post_from_spb,
    'post_from_nowhere': post_from_nowhere,
    'post_without_category': post_without_category,
    'booked_postst': booked_postst,
    'lost_posts': lost_posts,
  })