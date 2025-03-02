from django.urls import path

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name='groups'
urlpatterns = [
    path('detail/<int:pk>/follow/', subs_add, name='follow'),
    path('create/', community_create,name='group_create'),
    path('detail/<int:pk>/', community_detail,name='group_detail'),
    path('all/',all_groups,name='all'),
    path('detail/<int:pk>/delete/', PostDeleteGroups, name='delete'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)