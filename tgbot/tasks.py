import vk_api

from .services.posts_from_vk_creator import PostsFromVKCreator
from django.conf import settings

def fetch_posts_from_vk():
  login, password = settings.VK_LOGIN, settings.VK_PASS
  vk_session = vk_api.VkApi(login, password)
  try:
    vk_session.auth()
  except vk_api.AuthError as error_msg:
    print(error_msg)

  vk = vk_session.get_api()
  PostsFromVKCreator().create(vk)

  return True