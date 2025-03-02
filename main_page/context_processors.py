from django.contrib.auth.models import User
from messages_main.models import GlobalChat
from API.models import Song
def chat_messages(request):
    messages = GlobalChat.objects.order_by('-pub_date')[:50]
    return {'chat_messages':messages}
def song_list(request):
    songs=Song.objects.all()
    return {'songs_list':songs}
