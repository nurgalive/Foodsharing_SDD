from tgbot.models import User

def update_user_city(user_id, city):
  user_db = User.objects.filter(user_id__exact=str(user_id))

  user_db.update(city=city)