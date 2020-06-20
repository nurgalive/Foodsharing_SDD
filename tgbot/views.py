from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.decorators.csrf import csrf_exempt
import json

from utils.getCategory import get_food_category
from utils.gitCity import get_city
from utils.isBooked import is_booked
from .models import User, Message, Post, Group, Comment
from datetime import datetime
import vk_api

from .apps import TgbotConfig
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
    is_book = is_booked(text)
    category = get_food_category(text)


    try:
      Post.objects.get(post_id=post_id)
    except:
      group_id = group_id * -1
      group = Group.objects.get(group_id=group_id)
      result = Post.objects.create(
        post_id=post_id,
        text=text,
        posted_date=datetime.fromtimestamp(int(date)),
        link="https://vk.com/sharingfood?w=wall-"+str(group_id)+"_"+str(post_id)+"%2Fall",
        group_id=group,
        city=city.value,
        address="Default address",
        is_book=is_book,
        category=category
      )
    result.save()
  return redirect('home')





@csrf_exempt
def webhook(request, token):
  bot = TgbotConfig.registry.get_bot(token)
  
  if bot is None:
    bot = Bot(token)
    TgbotConfig.registry.add_bot(token, bot)

  # please insert magic here
  try:
    json_message = json.loads(request.body)
  except json.decoder.JSONDecodeError as err:
    return HttpResponse(str(err))

  def _update_id_exists(update_id: int) -> bool:
    if Message.objects.filter(update_id__exact=update_id).count() > 0:
      return True
    return False

  def _add_message_to_db(json_dict: dict) -> (None, True):
    try:
      sender_id     = json_dict['message']['from'].get('id')
      update_id     = json_dict.get('update_id')
      message_text  = json_dict['message'].get('text')
      message_date  = json_dict['message'].get('date')
    except KeyError:
      return None
    if None in (sender_id, update_id, message_text, message_date):
      return None

    if _update_id_exists(update_id):
      return True

    sender_object = None

    if User.objects.filter(user_id__exact=str(sender_id)).count() > 0:
      sender_object = User.objects.filter(user_id__exact=str(sender_id)).get()
    else:
      try:
        User(
          user_id = str(sender_id),
          first_name=json_dict['message']['from'].get('first_name'),
          last_name=json_dict['message']['from'].get('last_name'),
        ).save()
        sender_object = User.objects.filter(user_id__exact=str(sender_id)).get()
      except (KeyError, ValueError):
        return None

      try:
        Message(
          update_id=int(update_id),
          text=str(message_text),
          sender=sender_object,
          date=datetime.fromtimestamp(int(message_date)),
        ).save()
        return True
      except (KeyError, ValueError):
        return None

  try:
    result = _add_message_to_db(json_message)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
  if result is True:
    if bot is not None:
      bot.webhook(json.loads(request.body.decode('utf-8')))
      return HttpResponse('OK')
    else:
      raise Http404
    
  else:
    return HttpResponseBadRequest('Malformed or incomplete JSON data received')
