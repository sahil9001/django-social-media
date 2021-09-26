from users.models import FriendList
from posts.serializers import PostSerializer
from django.shortcuts import render
from .models import Posts
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def feed(request):
    try:
        friendlist = FriendList.objects.get(user=request.user)
    except ObjectDoesNotExist:
        friendlist = None
    
    post_list = []
    try:
        user_posts = Posts.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        user_posts = None

    if user_posts is not None:
        for post in user_posts.all():
            post_list.append(PostSerializer(post,context={'request':request}).data)

    if friendlist is not None:
        for friend in friendlist.friends.all():
            try:
                friend_posts = Posts.objects.filter(user=friend)
            except ObjectDoesNotExist:
                friend_posts = None
            if friend_posts is not None:
                for post in friend_posts.all():
                    post_list.append(PostSerializer(post,context={'request':request}).data)
    context = {
        'posts' : post_list
    }
    return render(request, 'users/home.html',context)