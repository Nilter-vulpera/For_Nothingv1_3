from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from groups.models import Groups
from datetime import datetime

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


# Create your models here.


# class AccountForUsers(models.Model):
#     username = models.OneToOneField(User, on_delete=models.CASCADE)
#     password = models.CharField(max_length=50,blank=True)
#     profile_pic = models.ImageField(null=True, upload_to="Profile/Profile")
#     backGround_pic = models.ImageField(null=True, upload_to="Profile/Background")





class FriendshipRequest(models.Model):
    REQUEST_STATUS = (
        ('NotFriends', 'Not a friends'),
        ('WaitingRequest', 'Waiting a request'),
        ('Accepted', 'Accepted'),
        ('Denied','Denied')
    )
    to_user = models.ForeignKey('auth.User',on_delete=models.CASCADE,
                                related_name="friendship_requests_to")
    from_user = models.ForeignKey('auth.User',on_delete=models.CASCADE,
                                  related_name="friendship_requests_from")
    status = models.CharField(max_length=25, choices=REQUEST_STATUS, default="Waiting a request")
    def accept(self):
        self.status='Accepted'
        self.save()
    def Denied(self):
        self.status='Denied'
        self.save()
    def Wait(self):
        self.status ="WaitingRequest"
        self.save()
    def __str__(self):
        return self.status

def user_directory_path(instance, filename):
    # Файлы будут загружены в MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/backgrounds/{1}/{2}/{3}/{4}'.format(instance.user.username,datetime.now().year,datetime.now().month,datetime.now().day ,filename)
class BackGround(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    background_img = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return self.user.username
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

# Create your models here.
class BotUser(models.Model):
    botuser = models.OneToOneField(User,on_delete=models.CASCADE)
    BotUserStatus = True

class photo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return self.user.username
class Block(models.Model):
    blocker = models.ForeignKey('auth.User', related_name='blocking', on_delete=models.CASCADE)
    blocked = models.ForeignKey('auth.User', related_name='blocked_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"


