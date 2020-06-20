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
        # page_id_obj = VkPage.objects.filter(page_link=private_page)[0]
        # result_private = CollectedData.objects.create(page_id=page_id_obj, subscribers=followers_count_private_page, posts=posts_private_page)
        # result_private.save()

#pprint(vk.wall.get(domain="sharingfood", count=1)['items'][0]['text'])

# получение id группы
#print(datetime.fromtimestamp(int(1592579330)))
