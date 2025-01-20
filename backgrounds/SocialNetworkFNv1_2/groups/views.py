# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .forms import *
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import *


def community_create(request):
    GroupsCreateform=GroupsCreate
    if request.method == 'POST':
        GroupsCreateform=GroupsCreate(request.POST, request.FILES)
        if GroupsCreateform.is_valid():
            name = request.POST['name']
            imgages = request.FILES['images']
            community = Groups.objects.create(name=name,images=imgages,AdminForGroups=request.user)
            community.save()
        return redirect('/', community=community.pk, admin=community.AdminForGroups)

    return render(request, 'flatpages/groups/create.html',
                  {'GroupCreateForm': GroupsCreate, 'GroupsCreateForm': GroupsCreateform})


def is_admin(request):
    if request.user.id == Groups.objects.AdminForGroups.all():
        is_admin1 = True
        print("Yeee")
    else:
        is_admin1 = False

    return render(request, 'flatpages/groups/detail.html', {'is_admin1': is_admin1})


def community_detail(request, pk):
    posts = Groups.get_posts(self=pk)
    community1 = get_object_or_404(Groups, pk=pk)
    GroupsImages=Groups.images
    form = PostForGroupsForm
    if request.method == 'POST':
        form = PostForGroupsForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.groupsPosts_id = pk
            p.user = request.user

            p.save()
        return redirect('groups:group_detail', pk=pk)
    AdminForGroup = community1.AdminForGroups.id
    return render(request, 'flatpages/groups/detail.html',
                  {'GroupAdmin1': AdminForGroup, 'community': community1, 'posts': posts, 'PostForm': form,
                   'pk': pk, 'GroupsImages':GroupsImages})


def PostDeleteGroups(request, pk):
    tag = PostForGroups.objects.get(pk=pk)
    if request.user == tag.user:
        tag.delete()
        return redirect('groups:group_detail', pk)


def all_groups(request):
    groups = Groups.objects.all()
    return render(request, 'flatpages/groups/GroupsAll.html', {'groups': groups})


def subs_add(request, pk):
    name = Groups.name
    g = Groups.objects.get(id=pk)
    g.subs.add(request.user)
    return redirect('groups:group_detail', pk)

def Add_Comment(request,pk):

    post = get_object_or_404(PostForGroups, id=pk)
    comments = PostMessages.get_comments.filter(self=pk)
    if request.method == 'POST':
        form = PostMessages1Form(request.POST)
        if form.is_valid():
            comments = form.save(commit=False)
            comments.post = post
            comments.save()
            return redirect("users:posts", post.id)
    else:
        form = PostMessages1Form()
    return render(request, 'flatpages/Posts/posts.html', {'posts': post,
                                                        'comments': comments,
                                                        'form': form})

# Определите представления для обновления и удаления сообществ по аналогии
