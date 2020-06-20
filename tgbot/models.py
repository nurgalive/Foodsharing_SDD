from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
  user_id     = models.IntegerField(unique=True, primary_key=True)
  first_name  = models.CharField(max_length=64)
  last_name   = models.CharField(max_length=64)

  def __str__(self):
      return f'{self.first_name} {self.last_name}'

class Message(models.Model):
  update_id = models.IntegerField(unique=True)
  text = models.TextField(max_length=4096)
  date = models.DateTimeField(default=timezone.now)
  sender = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
      return f'{self.text}'

class Group(models.Model):
  group_id= models.IntegerField(unique=True, primary_key=True)
  name = models.TextField(max_length=4096)
  link = models.URLField()
  city = models.TextField(max_length=32)

class Post(models.Model):
  post_id = models.IntegerField(unique=True, primary_key=True)
  text = models.TextField(max_length=4096, blank=True, null=True)
  posted_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
  link = models.URLField(blank=True, null=True)
  group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group", default=0)
  city = models.TextField(max_length=32, blank=True, null=True)
  address = models.TextField(max_length=4096, blank=True, null=True)


class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="group", default=0)
  text = models.TextField(max_length=4096)