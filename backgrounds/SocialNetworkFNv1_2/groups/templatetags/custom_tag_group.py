from django.contrib.auth.decorators import user_passes_test
from ..models import Groups
from django import template

register = template.Library()


@register.filter()
def is_group_admin(user):
    admin_group = Groups.AdminForGroups.get(user.id)
    return admin_group
