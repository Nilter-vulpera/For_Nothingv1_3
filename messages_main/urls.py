from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *
from . import consumers
app_name='messages_main'

from django.contrib.auth.decorators import login_required
from . import consumers
urlpatterns = [
    path('<int:message_id>/read/', mark_as_read, name='mark_as_read'),
    path(r'^dialogs/$', login_required(views.DialogsView.as_view()),name='dialogs'),
    path(r'^dialogs/create/(?P<chat_id>\d+)/(?<str:username>\d+)/', login_required(views.CreateDialogView.as_view()), name='createDialog'),
    path('dialogs/<int:chat_id>/<int:message_id>/<str:username>/', login_required(views.MessagesView.as_view()), name='messages'),
    path('chat/<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path('chat/create/', ChatCreateView.as_view(), name='chat_create'),
    path('chat/', ChatListView.as_view(), name='chat_list'),
    path('chats/', chat_list , name='few_chats_list'),
    # path('1234',select_color,name='main1234')
    path('chats/send_message/', views.send_message, name='send_message'),
    path('messages/<int:chat_id>/<int:message_id>/<str:username>/get_messages/', views.get_messages, name='get_messages'),
    #path('messages/chat/<int:chat_id>/send/', views.send_message_api, name='send_message_api'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

websocket_urlpatterns = [
    path('ws/chat/<str:chat_ids>/', consumers.ChatConsumer.as_asgi()),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




























