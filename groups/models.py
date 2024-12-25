from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Groups(models.Model):
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    subs = models.ManyToManyField(User, blank=True, related_name='subsForGroups')
    AdminForGroups = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')
    images=models.ImageField(upload_to="media/GroupsImages",default="media/backgrounds/ForNothing.jpg")
    def __str__(self):
        return self.name

    def get_posts(self):
        return PostForGroups.objects.filter(groupsPosts=self)


class PostForGroups(models.Model):
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to='media/GroupsPosts', blank=True)
    time_create = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    groupsPosts = models.ForeignKey(Groups, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def get_commentsForPosts(self):
        return PostMessages.objects.filter(Post=self)


class GroupMember(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_group_admin = models.BooleanField(default=False)


class PostMessages(models.Model):

    contentForPosts = models.TextField(default='')
    author_message_content = models.ForeignKey(User, verbose_name=("Пользователь"), on_delete=models.CASCADE, )
    pub_date = models.DateTimeField(('Дата сообщения'), default=timezone.now)
    Post = models.ForeignKey(PostForGroups,related_name="Posts", on_delete=models.deletion.CASCADE, null=True)

    def __str__(self):
        return f'{self.author_message_content} - {self.contentForPosts}'
    def get_commentsForPosts(self):
        return PostMessages.objects.filter(Post=self)
