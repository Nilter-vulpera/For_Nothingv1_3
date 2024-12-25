
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import re_path
app_name='users'

from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('block/<str:username>/', block_user, name='block_user'),
    path('unblock/<str:username>/', unblock_user, name='unblock_user'),

    path('', main),
    path('post/<int:pk>/', Add_Comment, name='posts'),

    path('post/<int:id>/delete/', PostDelete, name='delete'),
    path(r'^login/$',user_login,name='login'),
    path('logout/', LogoutView.as_view(template_name='flatpages/Account123/logout.html'), name='logout'),
    path('registretion/',
         register,
         name='registretion'),
    path('users/', AllUsers, name="AllUsers"),
    path('friends/', FriendUsers, name="FriendUsers"),
    # path('friends/request/<str:username>/', send_friend_request, name="send_friend_request"),
    path('friends/accept/<int:friendship_id>/', accept_friend_request, name="accept_friend_request"),
    path('friends/Denied/<int:friendship_id>/', Denied_friend_request, name="Denied_friend_request"),
    path('friends/Waiting/<int:id>/', Waiting_friend_request, name="Waiting_friend_request"),
    path('search/', search_users, name='search_users'),
    # path('user_profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
    path('friends/request/<str:username>/', send_friend_request, name='add_friend'),
    # path('user_profile/<int:pk>/', StatusForm.as_view(), name='StatusForm'),
    path('user_profile/<str:username>/', StatusForm, name='Profile'),
    path('license/',license,name="license"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


