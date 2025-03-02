from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse



def user_directory_path(instance, filename):
    # Файлы будут загружены в MEDIA_ROOT/user_<id>/<filename>
    return 'messages/{0}/{1}'.format(instance.author,filename)

class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )

    type = models.CharField(
        _('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    name = models.CharField(_('Name'), max_length=255, blank=True)
    members = models.ManyToManyField(User, verbose_name=_("Участник"))
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        ordering = ['type']
        
    def str(self):
        return f"Chat {self.id}"

    @property
    def last_message(self):
        return self.messages.order_by('-timestamp').first()

    def get_messages(self):
        return self.messages.all().order_by('timestamp')

#     OR

# @models.permalink
# def get_absolute_url(self):
#     return 'users:messages', (), {'chat_id': self.pk }

class Message(models.Model):
    COLOR_CHOICES = (
        ('red', 'red'),
        ('green', 'green'),
        ('blue', 'blue'),
        ('black', 'black'),
        ('white','white')
    )
    recipients = models.ManyToManyField(User, related_name='recipient')
    chat = models.ForeignKey(Chat, verbose_name=_("Чат"), on_delete=models.CASCADE, )
    author = models.ForeignKey('auth.User', verbose_name=_("Пользователь"), on_delete=models.CASCADE, )
    message = models.TextField(_("Сообщение"))
    pub_date = models.DateTimeField(_('Дата сообщения'), default=timezone.now)
    is_readed = models.BooleanField(_('Прочитано'), default=False)
    color = models.CharField(choices=COLOR_CHOICES, max_length=6, default="#f9f9f9")
    photoForMessages = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    
    class Meta:
        ordering = ['pub_date']

    def is_read_by_receiver(self):
        return self.read_statuses.filter(user=self.recipients, is_read=True).exists()


class MessageReadStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='read_statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
# Create your models here.

# class UserColor(models.Model):
#     COLOR_CHOICES = (
#         ('red', 'red'),
#         ('green', 'green'),
#         ('blue', 'blue'),
#         ('black', 'black')
#     )
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     color=models.CharField(max_length=7,default='red', choices=COLOR_CHOICES)

class GlobalChat(models.Model):

    content = models.TextField(_("Сообщения"))
    author_GC = models.ForeignKey(User, verbose_name=_("Пользователь"), on_delete=models.CASCADE, )
    pub_date = models.DateTimeField(_('Дата сообщения'), default=timezone.now)



