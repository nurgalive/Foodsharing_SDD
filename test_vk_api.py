import vk_api
from pprint import pprint
from datetime import datetime


login, password = '+4915205901185', '78ododad'
vk_session = vk_api.VkApi(login, password)
try:
        vk_session.auth()
except vk_api.AuthError as error_msg:
        print(error_msg)

vk = vk_session.get_api()


# comments = vk.wall.getComments(owner_id=-109125816, post_id=520093, count=100, sort='asc')

# count = comments['current_level_count']
# big_comment = ""
# for x in range(0,count):
#   try:
#     comments['items'][x]['deleted'] == True
#     continue
#   except:
#     text = comments['items'][x]['text']
#     #print(text)
#     big_comment = big_comment + text + " "

# print("Last comment id")
# last_comment_id = comments['items'][count-1]['id']
# print(count)
# print(big_comment)

for x in range(0,5):
  post = vk.wall.get(domain="sharingfood", count=5)
  text = post['items'][x]['text']
  date = post['items'][x]['date']
  id = post['items'][x]['id']
  group_id = post['items'][x]['owner_id']

  print(text)
  print(date)
  print(id)
  print(group_id)


#pprint(vk.wall.get(domain="sharingfood", count=1)['items'][0]['text'])

# получение id группы
#print(datetime.fromtimestamp(int(1592579330)))
