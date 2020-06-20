from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.decorators.csrf import csrf_exempt
import json

from utils.getCategory import get_food_category, all_cats
from utils.gitCity import get_city, get_metro_station
from utils.getIsBooked import get_is_booked
from utils.getIsLost import get_is_lost
from .models import User, Message, Post, Group, Comment, Category
from datetime import datetime
import vk_api

from .apps import TgbotConfig
from .services import MessageAndUserFromWebhookJSON
from .bot import Bot

def home(request):
  posts = Post.objects.all()
  return render(request, 'tgbot/home.html', {'posts' : posts})

def from_vk_to_db(request):
  login, password = '+4915205901185', '78ododad'
  vk_session = vk_api.VkApi(login, password)
  try:
    vk_session.auth()
  except vk_api.AuthError as error_msg:
    print(error_msg)

  vk = vk_session.get_api()

  for x in range(0,5):
    post = vk.wall.get(domain="sharingfood", count=5)
    text = post['items'][x]['text']
    date = post['items'][x]['date']
    post_id = post['items'][x]['id']
    group_id = post['items'][x]['owner_id']
    city = get_city(text)
    is_book = get_is_booked(text)
    category = get_food_category(text)
    is_lost = get_is_lost(text)
    metro = get_metro_station(text)

    try:
      Post.objects.get(post_id=post_id)
    except:
      group_id = group_id * -1
      group = Group.objects.get(group_id=group_id)

      comments = vk.wall.getComments(owner_id=group_id, post_id=post_id, count=100, sort='asc')

      count = comments['current_level_count']
      big_comment = ""
      for x in range(0,count):
        try:
          comments['items'][x]['deleted'] == True
          continue
        except:
          text = comments['items'][x]['text']
          #print(text)
          big_comment = big_comment + text + " "

      # last comment id
      last_comment_id = comments['items'][count-1]['id']
      # resulted comment
      #print(big_comment)

      result = Post.objects.create(
        post_id=post_id,
        text=text,
        posted_date=datetime.fromtimestamp(int(date)),
        link="https://vk.com/sharingfood?w=wall-"+str(group_id)+"_"+str(post_id)+"%2Fall",
        group_id=group,
        city=city.value,
        address="Default address",
        is_book=is_book,
        category=category,
        is_lost=is_lost,
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
    json_message = json.loads(json.loads(request.body.decode('utf-8')))
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
