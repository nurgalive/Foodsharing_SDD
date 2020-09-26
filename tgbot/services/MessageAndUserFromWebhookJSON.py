from tgbot.models import User, Message

from datetime import datetime

# Класс для сохранения информации о юзере и сообщении в БД
class MessageAndUserFromWebhookJSON:
  def save(self, json_dict: dict) -> (None, True):
    try:
      sender_id     = json_dict['message']['from'].get('id')
      update_id     = json_dict.get('update_id')
      message_text  = json_dict['message'].get('text')
      message_date  = json_dict['message'].get('date')
    except KeyError:
      return None
    if None in (sender_id, update_id, message_text, message_date):
      return None

    if Message.objects.filter(update_id__exact=update_id).count() > 0:
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
