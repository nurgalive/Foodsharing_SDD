from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'group_id', 'posted_date', 'city', 'metro']
    search_fields = ['post_id', 'text', 'city', 'metro', 'address', 'category']
    #readonly_fields = []
    #filter_horizontal = []
    list_filter = ['category', 'group_id', 'city', 'metro']
    # fieldsets = []

#   post_id     = models.IntegerField(unique=True, primary_key=True)
#   text        = models.TextField(max_length=4096, blank=True, null=True)
#   posted_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
#   link        = models.URLField(blank=True, null=True)
#   group_id    = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group", default=0)
#   city        = models.TextField(max_length=32, blank=True, null=True)
#   metro       = models.TextField(max_length=128, blank=True, null=True)
#   address     = models.TextField(max_length=4096, blank=True, null=True)
#   category    = models.TextField(max_length=64, blank=True, null=True)
#   is_book     = models.BooleanField(default=False)
#   is_lost     = models.BooleanField(default=False)

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(UserToCategory)
