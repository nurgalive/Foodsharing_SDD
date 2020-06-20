from django.urls import re_path, path
from . import views
from .views import webhook

urlpatterns = [
  path('', views.home, name='home'),
  path('from_vk_to_db', views.from_vk_to_db, name='from_vk_to_db'),
  re_path(r'^bot/(?P<token>.+)/', webhook),
]