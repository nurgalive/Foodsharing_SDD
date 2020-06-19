from django.urls import path
from edudam.tgbot import views

urlpatterns = [
    path('webhook/', views.webhook_message),
]