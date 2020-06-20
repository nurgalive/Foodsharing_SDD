from django.contrib import admin
from .models import User, Message, Comment, Post, Group

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Post)
