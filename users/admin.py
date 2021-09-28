from django.contrib import admin
from .models import FriendList, FriendRequest, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(FriendList)
admin.site.register(FriendRequest)
