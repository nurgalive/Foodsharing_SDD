from django.urls import re_path
from . import views

from .views import webhook_message

urlpatterns = [
  re_path(r'webhook/(?P<token>.+)/', webhook_message),
]