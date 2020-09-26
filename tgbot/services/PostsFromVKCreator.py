from tgbot.models import User, Message, Group, Post
from datetime import datetime

from tgbot.machine_learning.get_category import get_food_category, all_cats
from tgbot.machine_learning.get_city import get_city, get_metro_station
from tgbot.machine_learning.get_is_booked import get_is_booked
from tgbot.machine_learning.get_is_lost import get_is_lost
from datetime import datetime

class PostsFromVKCreator:
  def create(self, vk):
    groups = Group.objects.all()
    for group in groups:
      domain = group.link[15:len(group.link)]
      posts = vk.wall.get(domain=domain, count=100)
      for x in range(0,100):
        if posts['items'][x] is None:
          continue

        text = posts['items'][x]['text']
        date = posts['items'][x]['date']
        post_id = posts['items'][x]['id']
        group_id = posts['items'][x]['owner_id']
        city = get_city(text)
        is_book = get_is_booked(text)
        category = get_food_category(text)
        is_lost = get_is_lost(text)
        metro = get_metro_station(text)

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
