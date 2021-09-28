from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.
class Users(AbstractUser):
    USERNAME_FIELD = "phone"
    fullname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=50, unique=True, blank=False)
    occupation = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=255, null=True)
    dob = models.DateField(default=date.today)
    password = models.CharField(max_length=255)
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.fullname


class FriendList(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    friends = models.ManyToManyField(Users, blank=True, related_name="friends")

    def __str__(self):
        return self.user.fullname

    def add_friend(self, account):
        """
        Add a friend to the list
        """
        if not account in self.friends.all():
            self.friends.add(account)
            return True

    def remove_friend(self, account):
        """
        Remove a friend from the list
        """
        if account in self.friends.all():
            self.friends.remove(account)
            return True

    def unfriend(self, removee):
        """
        Unfriend someone
        """
        remover_friends_list = self
        remover_friends_list.remove_friend(removee)
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    """
    1. Sender,
    2. Receiver
    """

    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="receiver"
    )
    is_active = models.BooleanField(default=True, blank=True, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.fullname + " " + self.receiver.fullname

    def accept(self):
        """
        Accept friend request
        """
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """
        Decline a friend request
        """
        self.is_active = False
        self.save()

    def cancel(self):
        """
        Cancel from sender side
        """
        self.is_active = False
        self.save()
