"""djangoproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views
from posts import views as post_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("register", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("feed/", post_views.feed, name="feed"),
    path("friendrequest/", views.friendrequest, name="friend-requests"),
    path("profile/<int:id>",views.otherprofile, name="other-profile"),
    path('send_request/', views.send_friend_request, name='send-friend-request'),
    path('accept_request/', views.accept_friend_request, name='accept-friend-request'),
    path('decline_request/', views.decline_friend_request, name='decline-friend-request'),
    path('friend_list/', views.friend_list, name='friend-list'),
    path('remove_friend/', views.remove_friend, name='remove-friend'),
    path('remove_post/',views.remove_post,name="remove-post"),
    path('new_post/',views.new_post,name="new-post")
]
