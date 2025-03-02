from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import main
from messages_main.views import chat_view
from API.views import song_list123
app_name='main_page'
urlpatterns = [
    path('',chat_view,name='main'),
    path('',song_list123,name='song_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
