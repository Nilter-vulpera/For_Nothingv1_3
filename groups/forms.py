from django import forms
from .models import Groups, PostForGroups, PostMessages
from django.forms import ModelForm


class GroupsCreate(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ['name', 'images']


class PostForGroupsForm(forms.ModelForm):
    class Meta:
        model = PostForGroups
        fields = ['content', 'photo']


class addSubscribe(forms.ModelForm):
    class Meta:
        model: Groups
        fields = ['subs']


class PostMessages1Form(forms.ModelForm):
    class Meta:
        model = PostMessages
        fields = ['contentForPosts']
