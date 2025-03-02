from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,re_path
from .views import chat
app_name='chatbot'
urlpatterns = [
    path(r'^ChatBotresponse/', chat, name='chat'),
    path(r'^ChatBotresponse\d+)/$', chat, name='chat1'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)