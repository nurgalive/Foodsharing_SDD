import vk_api

login, password = '+4915205901185', '78ododad'
vk_session = vk_api.VkApi(login, password)
try:
        vk_session.auth()
except vk_api.AuthError as error_msg:
        print(error_msg)

vk = vk_session.get_api()

print(vk.wall.get(owner_id="https://vk.com/sharingfood"))

#vk.groups.wall.get("https://vk.com/sharingfood")


# artists = Artist.objects.all()
# for artist in artists:
# print(artist.artist_name)
# private_page = artist.vk_private_page.page_link
# print(private_page)
# group_page = artist.vk_group_page.page_link
# print(group_page)
# vk_group_id_nickname = group_page[15:len(group_page)]
# group_members = vk.groups.getMembers(group_id=vk_group_id_nickname)['count']
# vk_group_id = vk.groups.getById(group_id=vk_group_id_nickname)[0]['id']
# print(group_members)
# posts_group = vk.wall.get(owner_id='-' + str(vk_group_id))['count']
# print(posts_group)
# vk_private_page = private_page[15:len(private_page)]
# check = False
# try:
#         int(vk_private_page)
#         check = True
# except ValueError:
#         check = False
# if (check==False):
#         vk_private_page = vk.users.get(user_ids=vk_private_page)[0]['id']

# followers_count_private_page = vk.users.get(user_ids=vk_private_page, fields='followers_count')[0]['followers_count']
# posts_private_page = vk.wall.get(owner_id=vk_private_page)['count']
# print(followers_count_private_page)
# print(posts_private_page)

# page_id_obj = VkPage.objects.filter(page_link=group_page)[0]
# result_group = CollectedData.objects.create(page_id=page_id_obj, subscribers=group_members, posts=posts_group)
# result_group.save()

# page_id_obj = VkPage.objects.filter(page_link=private_page)[0]
# result_private = CollectedData.objects.create(page_id=page_id_obj, subscribers=followers_count_private_page, posts=posts_private_page)
# result_private.save()