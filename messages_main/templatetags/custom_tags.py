from django import template
register = template.Library()

from messages_main.models import *


@register.simple_tag
def get_companion(user, chat):
    if chat.type == 'D':
        for u in chat.members.all():
            if u != user:
                return u


