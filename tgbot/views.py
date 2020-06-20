from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Message
from datetime import datetime

from .apps import TgbotConfig
from telegram import Bot as TelegramBot

# Create your views here.
@csrf_exempt
def webhook(request, token):
    bot = TgbotConfig.registry.get_bot(token)
    if bot is None:
      bot = TelegramBot(token)
      TgbotConfig.registry.add_bot(token, bot)
    
    if bot is not None:
        bot.webhook(json.loads(request.body.decode('utf-8')))
        return HttpResponse()
    else:
        raise Http404

  # # please insert magic here
  # try:
  #   json_message = json.loads(request.body)
  # except json.decoder.JSONDecodeError as err:
  #   return HttpResponse(str(err))

  # def _is_user_registered(user_id: int) -> bool:
  #   if User.objects.filter(user_id__exact=user_id).count() > 0:
  #     return True
  #   return False

  # def _update_id_exists(update_id: int) -> bool:
  #   if Message.objects.filter(update_id__exact=update_id).count() > 0:
  #     return True
  #   return False

  # def _add_message_to_db(json_dict: dict) -> (None, True):
  #   try:
  #     sender_id     = json_dict['message']['from'].get('id')
  #     sender_object = User.objects.filter(user_id__exact=sender_id).get()
  #     update_id     = json_dict.get('update_id')
  #     message_text  = json_dict['message'].get('text')
  #     message_date  = json_dict['message'].get('date')
  #   except KeyError:
  #     return None
  #   if None in (sender_id, update_id, message_text, message_date):
  #     return None

  #   if _update_id_exists(update_id):
  #     return True

  #   if _is_user_registered(sender_id):
  #     try:
  #       Message(
  #         update_id=int(update_id),
  #         text=str(message_text),
  #         sender=sender_object,
  #         date=datetime.fromtimestamp(int(message_date)),
  #       ).save()
  #       return True
  #     except (KeyError, ValueError):
  #       return None
  #   else:
  #     raise ValueError('Sender is rejected')

  # try:
  #   result = _add_message_to_db(json_message)
  # except ValueError as e:
  #   return HttpResponseBadRequest(str(e))
  # if result is True:
  #   return HttpResponse('OK')
  # else:
  #   return HttpResponseBadRequest('Malformed or incomplete JSON data received')
