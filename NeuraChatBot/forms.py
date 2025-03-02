from django import forms
from .models import message_to_chat_bot
from django.forms import ModelForm

class MessageFormForBot(forms.ModelForm):
    # context_field = forms.CharField(label='Контекст', widget=forms.Textarea)
    # question_field = forms.CharField(label='Вопрос', max_length=100)

    class Meta:
        model = message_to_chat_bot
        fields = ['message_to_chat_bot_text']
