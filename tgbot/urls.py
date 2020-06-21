from django.urls import re_path, path
from . import views
from .views import webhook

# Список страниц и эндпоинтов приложения
urlpatterns = [
  path('', views.home, name='home'),
  path('analytic', views.analytic, name='analytic'),
  path('from_vk_to_db', views.from_vk_to_db, name='from_vk_to_db'),
  path('upload_cats_to_db', views.upload_cats_to_db, name='upload_cats_to_db'),
  path('notify_users', views.notify_users, name='notify_users'),
  re_path(r'^bot/(?P<token>.+)/', webhook),
]