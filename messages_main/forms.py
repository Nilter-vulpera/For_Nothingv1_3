from django import forms
from .models import *
from django.forms import ModelForm


class MessageForm1234(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message', 'color', 'photoForMessages']


class ChatForm1234(forms.ModelForm):
    class Meta:
        model = GlobalChat
        fields = ['content']

class ChatForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Choose friends to add"
    )

    class Meta:
        model = Chat
        fields = ['type', 'name', 'members']

    def clean(self):
        cleaned_data = super().clean()
        chat_type = cleaned_data.get("type")
        name = cleaned_data.get("name")

        if chat_type == 'C' and not name:
            self.add_error('name', "Должно быть название чата")
        return cleaned_data


#
#     class Meta:
#         COLOR_CHOICES = (
#             ('red', 'red'),
#             ('green', 'green'),
#             ('blue', 'blue'),
#             ('black', 'black')
#         )
#         color = forms.ChoiceField(choices=COLOR_CHOICES)
#         model = UserColor
#         fields=['color']
