from django.contrib.auth.models import User

from .models import FriendshipRequest


def friends_list(request):
    if request.user.is_authenticated:
        friends = FriendshipRequest.objects.filter(to_user=request.user,
                                                   status='Accepted').values_list('from_user',
                                                                                  flat=True)
        friends = User.objects.filter(id__in=friends)
        return {'friends_list': friends}
    return {'friends_list': []}