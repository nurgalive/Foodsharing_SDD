from django.urls import re_path, path
from . import views
from .views import webhook

urlpatterns = [
  path('', views.home, name='home'),
  path('from_vk_to_db', views.from_vk_to_db, name='from_vk_to_db'),
  path('upload_cats_to_db', views.upload_cats_to_db, name='upload_cats_to_db'),
  path('notify_users', views.notify_users, name='notify_users'),
  re_path(r'^bot/(?P<token>.+)/', webhook),
]