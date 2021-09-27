from posts.models import Posts
from django.shortcuts import render
from users.forms import NewPostForm, SignInForm, SignUpForm
from django.shortcuts import render, redirect
import requests
from djangoproj import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .serializers import CreateFormSerializer, UserLoginSerializer, UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from .models import FriendList, FriendRequest, Users
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# def authenticate(request):
#     try:
#         user = Users.objects.get(phone=request["phone"])
#     except ObjectDoesNotExist:
#         return None
#     if user.check_password(request["password"]):
#         return user
#     return None


def login_user(request, data):
    serializer = UserLoginSerializer(data=data)
    if serializer.is_valid():
        found_phone = serializer.data["phone"]

        user = authenticate(phone=found_phone, password=data["password"])
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            request.user = user
            return Response({"token": f"Token {token.key}"}, status.HTTP_202_ACCEPTED)
        else:
            try:
                if Users.objects.get(phone=found_phone):
                    return Response(
                        {"detail": "Credentials did not match"},
                        status.HTTP_401_UNAUTHORIZED,
                    )

            except Users.DoesNotExist:
                return Response({"detail": "User not found"}, status.HTTP_404_NOT_FOUND)
    else:
        data = serializer.errors
        return Response(data, status.HTTP_400_BAD_REQUEST)


def register_user(request, data):
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        friendlist, flag = FriendList.objects.get_or_create(user=user)
        friendlist.save()
        return Response({}, status.HTTP_201_CREATED)
    else:
        data = serializer.errors
        return Response(data, status.HTTP_400_BAD_REQUEST)


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data.get("fullname")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            phone = form.cleaned_data.get("phone")
            address = form.cleaned_data.get("address")
            occupation = form.cleaned_data.get("occupation")
            dob = form.cleaned_data.get("dob")
            form_obj = {
                "fullname": fullname,
                "username": username,
                "email": email,
                "password": password,
                "phone": phone,
                "address" : address,
                "occupation" : occupation,
                "dob" : dob
            }
            response = register_user(request, data=form_obj)
            if response.status_code == 201:
                return redirect("feed")
            else:
                messages.warning(request, "User already exists")
    else:
        form = SignUpForm()
    return render(request, "users/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password")
            form_obj = {
                "phone": phone,
                "password": password,
            }
            response = login_user(request, data=form_obj)
            if response.status_code == 202:
                return redirect("feed")
            else:
                messages.warning(request, "Credentials don't match")
    else:
        form = SignInForm()
    return render(request, "users/login.html", {"form": form})


@login_required
def logout(request):
    return render(request, "users/logout.html")


@login_required
def profile(request):
    try:
        posts = Posts.objects.filter(user=request.user)
    except Posts.DoesNotExist:
        posts = None

    try:
        friendlist = FriendList.objects.get(user=request.user)
    except FriendList.DoesNotExist:
        friendlist = None
    post_list = []
    friend_list = []
    if posts:
        for post in posts:
            post_list.append(post)
    if friendlist:
        for friend in friendlist.friends.all():
            friend_list.append(friend)
    friend_request_list = []
    try:
        friendrequest = FriendRequest.objects.filter(receiver=request.user)
    except FriendRequest.DoesNotExist:
        friendrequest = None
    if friendrequest:
        for req in friendrequest:
            friend_request_list.append(req)
    return render(
        request, "users/profile.html", {"friendrequest" : friend_request_list,"posts": post_list, "friends": friend_list}
    )


@login_required
def friendrequest(request):
    friendrequest_obj = FriendRequest.objects.filter(receiver=request.user)
    friendrequest_list = []
    if friendrequest_obj:
        for friendrequest in friendrequest_obj.all():
            if friendrequest.is_active:
                friendrequest_list.append(friendrequest)
    return render(
        request, "users/friendrequests.html", {"friendrequests": friendrequest_list}
    )


@login_required
def otherprofile(request, id):
    try:
        user = Users.objects.get(pk=id)
    except Users.DoesNotExist:
        user = None
    try:
        friendlist = FriendList.objects.get(user=user)
    except FriendList.DoesNotExist:
        friendlist = None
    is_friend = False
    if friendlist and user:
        if user in friendlist.friends.all():
            is_friend = True
    mutual_friends = []
    all_friends = []
    if friendlist and user:
        for friend in friendlist.friends.all():
            if friendlist.is_mutual_friend(user):
                mutual_friends.append(friend)
            all_friends.append(friend)
    if user == request.user:
        is_friend = True
    try:
        posts = Posts.objects.filter(user=user)
    except Posts.DoesNotExist:
        posts = None
    post_list = []
    if posts:
        for post in posts:
            post_list.append(post)
    return render(
        request,
        "users/otherprofile.html",
        {
            "user": user,
            "is_friend": is_friend,
            "mutual_friends": mutual_friends,
            "friends": all_friends,
            "posts" : post_list
        },
    )


@login_required
@csrf_exempt
def send_friend_request(request):
    if request.method == "POST":
        receiver_id = request.POST.get("user_id")
        try:
            receiver = Users.objects.get(pk=receiver_id)
        except Users.DoesNotExist:
            receiver = None
        if receiver:
            friendrequest, flag = FriendRequest.objects.get_or_create(
                sender=request.user, receiver=receiver
            )
            friendrequest.save()
            messages.success(request, "Friend request sent")
            return redirect("friend-requests")
        else:
            messages.warning(request, "User not found")
            return redirect("friend-requests")
    else:
        return redirect("friend-requests")


@login_required
@csrf_exempt
def accept_friend_request(request):
    if request.method == "POST":
        try:
            user = Users.objects.get(pk=request.POST.get("friendrequest_id"))
        except Users.DoesNotExist:
            user = None
        try:
            friendrequest = FriendRequest.objects.get(
                sender=user, receiver=request.user
            )
        except FriendRequest.DoesNotExist:
            friendrequest = None
        if friendrequest:
            friendrequest.accept()
            friendrequest.save()
            messages.success(request, "Friend request accepted")
            return redirect("friend-requests")
        else:
            messages.warning(request, "Friend request not found")
            return redirect("friend-requests")

    else:
        return redirect("friend-requests")


@login_required
@csrf_exempt
def decline_friend_request(request):
    if request.method == "POST":
        try:
            user = Users.objects.get(pk=request.POST.get("friendrequest_id"))
        except Users.DoesNotExist:
            user = None
        try:
            friendrequest = FriendRequest.objects.get(
                sender=request.user, receiver=user
            )
        except FriendRequest.DoesNotExist:
            friendrequest = None
        if friendrequest:
            friendrequest.decline()
            friendrequest.save()
            messages.success(request, "Friend request accepted")
            return redirect("friend-requests")
        else:
            messages.warning(request, "Friend request not found")
            return redirect("friend-requests")

    else:
        return redirect("friend-requests")


@login_required
def friend_list(request):
    try:
        friendlist = FriendList.objects.get(user=request.user)
    except FriendList.DoesNotExist:
        friendlist = None

    if friendlist:
        friends = friendlist.friends.all()
        mutual_friends = []
        for friend in friends:
            if friendlist.is_mutual_friend(friend):
                mutual_friends.append(friend)

        return render(
            request,
            "users/friends.html",
            {"friends": friends, "mutual_friends": mutual_friends},
        )
    else:
        return render(request, "users/friends.html")


@login_required
@csrf_exempt
def remove_friend(request):
    if request.method == "POST":
        try:
            friendlist = FriendList.objects.get(user=request.user)
        except FriendList.DoesNotExist:
            friendlist = None

        try:
            user = Users.objects.get(pk=request.POST.get("friend_id"))
        except Users.DoesNotExist:
            user = None

        if friendlist:
            friendlist.unfriend(user)
            friendlist.save()
            messages.success(request, "Friend removed")
            return redirect("friend-list")
        else:
            messages.warning(request, "Friend not found")
            return redirect("friend-list")
    else:
        return redirect("friend-list")

@login_required
@csrf_exempt
def remove_post(request):
    if request.method == "POST":
        try:
            post = Posts.objects.get(pk = request.POST.get("post_id"))
        except Posts.DoesNotExist:
            post = None
        
        if post:
            post.delete()
            messages.success(request,"Post Deleted Successfully")
            return redirect("profile")
        else:
            messages.warning(request,"Unable to delete post")
            return redirect("profile")
    else:
        return redirect("profile")

def create_post(request,data):
    serializer = CreateFormSerializer(data=data)
    if serializer.is_valid():
        post = serializer.save(user=request.user)
        return Response({}, status.HTTP_201_CREATED)
    else:
        data = serializer.errors
        print(data)
        return Response(data, status.HTTP_400_BAD_REQUEST)

@login_required
def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            body = form.cleaned_data.get("body")
            image = form.cleaned_data.get("image")
            form_obj = {
                "title" : title,
                "body" : body,
                "image" : image,
            }
            response = create_post(request, data=form_obj)
            print(response.status_code)
            if response.status_code == 201:
                messages.success(request,"Posted successfully!")

                return redirect("new-post")
            else:
                messages.warning(request, "Credentials don't match")
    else:
        form = NewPostForm()
    return render(request, "users/new_post.html", {"form": form})
