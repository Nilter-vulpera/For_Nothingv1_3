from django.contrib.auth.models import User

from .models import FriendshipRequest, MisconductUser

def misconduct_users(request):
       bad_users = MisconductUser.objects.filter(reason__icontains='сквернословие')
       return {'bad_users': bad_users}
       
       
def friends_list(request):
    if request.user.is_authenticated:
        friends = FriendshipRequest.objects.filter(to_user=request.user,
                                                   status='Accepted').values_list('from_user',
                                                                                  flat=True)
        friends = User.objects.filter(id__in=friends)
        return {'friends_list': friends}
    return {'friends_list': []}
