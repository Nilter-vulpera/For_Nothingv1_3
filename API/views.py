
from django.shortcuts import render
from .models import Song

def song_list123(request):
    songs = Song.objects.all()
    return render(request, 'flatpages\main\html\main.html', {'songs123': songs})
# Create your views here.
