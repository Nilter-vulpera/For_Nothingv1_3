from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.views import View

from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404

from groups.models import PostForGroups, Groups, PostMessages

from groups.forms import PostMessages1Form
from django.db.models import Count, Q
from .forms import *
from .models import *
from django.contrib.auth.models import User

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib import messages
from django.views.generic.detail import DetailView

from messages_main.models import Chat, Message

from messages_main.forms import MessageForm1234
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

class Login(LoginView):
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


# Create your views here.
class Logout(LoginView):
    def logout_request(request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("main:homepage")


def register(request):
    if request.method == 'POST':
        form = BaseRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('main_page:main')  # Перенаправьте на страницу после успешной регистрации
    else:
        form = BaseRegisterForm()

    return render(request, 'flatpages/Account123/registretion.html', {'form': form})


# Create your views here.
@login_required
def FriendUsers(request):
    user = request.user.id
    received_requests = FriendshipRequest.objects.filter(to_user=user, status='Waiting a request')
    accepted_friend_request = FriendshipRequest.objects.filter(to_user=user, status='Accepted')
    return render(request, 'flatpages/Account123/friends_accounts.html',
                  {'received_requests': received_requests, 'accepted_friend_request': accepted_friend_request})


@login_required
def add_friend(request, username):
    user_to_add = get_object_or_404(User, username=username)
    if FriendshipRequest.objects.filter(from_user=request.user, to_user=user_to_add).exists():
        return JsonResponse({'message': 'Already friends'}, status=400)
    if user_to_add == request.user:
        return JsonResponse({'message': 'Cannot add yourself'}, status=400)

    friendship = FriendshipRequest(from_user=request.user, to_user=user_to_add)
    friendship.status = "Waiting a request"
    friendship.save()

    return JsonResponse({'message': 'Friend add successfully'})


@login_required
def send_friend_request(request, username):
    from_user = request.user
    to_user = get_object_or_404(User, username=username)
    if FriendshipRequest.objects.filter(from_user=request.user, to_user=to_user, status='Accepted').exists():
        return JsonResponse({'message': 'Already friends'}, status=400)
    if FriendshipRequest.objects.filter(from_user=request.user, to_user=to_user, status='Denied').exists():
        return JsonResponse({'message': 'Denied request'}, status=400)
    if FriendshipRequest.objects.filter(from_user=request.user, to_user=to_user, status='Not a friends').exists():
        return JsonResponse({'message': 'Not friends'}, status=400)
    if FriendshipRequest.objects.filter(from_user=request.user, to_user=to_user, status='Waiting a request').exists():
        return JsonResponse({'message': 'Waiting a request'}, status=400)
    friendship_request = FriendshipRequest(from_user=from_user, to_user=to_user, status='Waiting a request')
    friendship_request.save()

    return redirect('users:FriendUsers')


@login_required
def accept_friend_request(request, friendship_id):
    friendship = get_object_or_404(FriendshipRequest, id=friendship_id)
    friendship.accept()
    return redirect('users:FriendUsers')


@login_required
def Denied_friend_request(request, friendship_id):
    friendship = get_object_or_404(FriendshipRequest, id=friendship_id)
    friendship.Denied()
    return redirect('users:FriendUsers')


@login_required
def Waiting_friend_request(request, friendship_id):
    friendship = get_object_or_404(FriendshipRequest, id=friendship_id)
    friendship.Wait()
    friendship.save()
    return render(request, 'flatpages/Account123/accounts.html', {"friendship": friendship})


def main(request):
    return render(request, 'flatpages/main/html/main.html')


def AllUsers(request):
    form = UserSearchForm()
    results = []
    if request.method == 'GET' and 'query' in request.GET:
        form = UserSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            user_list = User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
            paginator = Paginator(user_list, 10)  # 10 результатов на страницу
            page = request.GET.get('page')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
    users_list = User.objects.all()
    context = {
        "users_list": users_list,
        "form":form,
        "results":results,
        # "profile_image": account.profile_image,
    }
    return render(request, 'flatpages/Account123/accounts.html', context)

    # status = get_object_or_404(FriendshipRequest, id=self.kwargs['pk'])
    # statusForm = friendChoiceForm  # Создаем экземпляр нашей формы
    # return render(request, 'flatpages/Account123/account.html', {'statusForm': statusForm, 'status': status})


@login_required
def post(request):
    user = request.user
    user_groups = Groups.objects.filter(subs=user)
    newsOnMain = PostForGroups.objects.filter(groupsPosts__in=user_groups)
    form = PostMessages1Form(request.POST)
    comments1 = PostMessages.get_commentsForPosts(self=1)
    if form.is_valid():
        comments = form.save(commit=False)
        comments.post = newsOnMain
        comments.save()
        return redirect("users:posts", request.user.pk)
    return render(request, 'flatpages/Posts/posts.html', {'posts': newsOnMain,
                                                          'form': form,
                                                          'comments': comments1,
                                                          })


@login_required
def Add_Comment(request, pk):
    user = request.user
    user_groups = Groups.objects.filter(subs=user)
    newsOnMain = PostForGroups.objects.filter(groupsPosts__in=user_groups)
    post = get_object_or_404(PostForGroups, id=pk)
    comments1 = PostMessages.objects.filter(Post=post).order_by('pub_date')
    if request.method == 'POST':
        form = PostMessages1Form(request.POST)
        if form.is_valid():
            comments = form.save(commit=False)
            comments.user = request.user
            comments.Post = post
            comments.save()
            return redirect("users:posts", pk=pk)
    else:
        form = PostMessages1Form()
    return render(request, 'flatpages/Posts/posts.html', {'posts': newsOnMain,
                                                          'comments': comments1,
                                                          'form': form})


# class ShowProfilePageView(DetailView):
#     model = User
#     template_name = 'flatpages/Account123/account.html'
#
#     def get_context_data(self, *args, **kwargs):
#         statusForm = friendChoiceForm
#         users = User.objects.all()
#         context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
#         page_user = get_object_or_404(User, id=self.kwargs['pk'])
#         context['page_user'] = page_user
#
#         return context


def user_login(request):
    Loginform = LoginForm(request.POST)
    if request.method == 'POST':

        if Loginform.is_valid():
            cd = Loginform.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('main_page:main')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, 'Invalid login.')
                return render(request, 'flatpages/Account123/login.html', {})
    return render(request, 'flatpages/Account123/login.html', {'Loginform': Loginform})


def PostDelete(request, id):
    tag = PostForGroups.objects.get(pk=id)
    if request.user == tag.user:
        tag.delete()
        return render(request, 'flatpages/Posts/posts.html', {'tag': tag})


def profile(request):
    profiles = request.user.profile
    ImageForm = BackgroundImageForm(instance=profiles)
    if request.method == "POST":
        ImageForm = BackgroundImageForm(request.POST, request.FILES, instance=profiles)
        if ImageForm.is_valid():
            ImageForm.save()
            return redirect('profile')
    return render(request, 'flatpages/Account123/account.html', {'profile': profiles,
                                                                 'ImageForm': ImageForm
                                                                 })


@login_required
def StatusForm(request, username):
    MessageForm = MessageForm1234()
    user = get_object_or_404(User, username=username)  # Получаем пользователя по его имени
    backgrounded = BackGround.background_img
    avatarka = photo.photo
    recipient = get_object_or_404(User, username=username)
    chats = Chat.objects.filter(
        type=Chat.DIALOG,
        members=request.user
    ).filter(
        members=recipient
    ).distinct()

    if chats.exists():
        chat = chats.first()
    else:
        # Создаем новый чат, если он не существует
        chat = Chat.objects.create(type=Chat.DIALOG)
        chat.members.add(request.user)
        chat.members.add(recipient)
        chat.save()

    # Добавим проверку и логгирование перед вызовом reverse

    try:
        friendship = FriendshipRequest.objects.get(
            from_user=request.user,
            to_user=user
        )  # Получаем дружбу между текущим пользователем и пользователем страницы
        status = friendship.status
    except FriendshipRequest.DoesNotExist:
        status = "Not a Friends"

    try:
        account = request.user.background
    except BackGround.DoesNotExist:
        account = BackGround(user=request.user)

    is_blockedByUou = Block.objects.filter(
        blocker=request.user,
        blocked=recipient
    ).exists() if request.user.is_authenticated else False
    is_blockedByEnemy = Block.objects.filter(
        blocker=recipient,
        blocked=request.user
    ).exists() if request.user.is_authenticated else False

    if request.method == 'POST':
        form = BackgroundImageForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()
            return redirect('users:Profile', request.user.username)
    else:
        form = BackgroundImageForm(instance=account)

    if request.method == 'POST':
        avatarkaForm = AvatarImgForm(request.POST, request.FILES, instance=account)
        if avatarkaForm.is_valid():
            avatarkaForm.save()
            return redirect('users:Profile', request.user.username)
    else:
        avatarkaForm = AvatarImgForm(instance=account)

    return render(request, 'flatpages/Account123/account.html',
                  {'status': status, 'page_user': user, 'avatarkaForm': avatarkaForm, 'ImageForm': form,
                   'backgrounded': backgrounded, 'avatarka': avatarka,
                   'is_blockedByEnemy': is_blockedByEnemy, 'is_blockedByUou': is_blockedByUou,
                   'chatFromUser': chat,
                   'recipient': recipient, 'Messageform': MessageForm})


def block_user(request, username):
    blocker = request.user
    blocked = User.objects.get(username=username)
    Block.objects.get_or_create(blocker=blocker, blocked=blocked)
    return redirect('users:Profile', username=username)


def unblock_user(request, username):
    blocker = request.user
    blocked = User.objects.get(username=username)
    Block.objects.filter(blocker=blocker, blocked=blocked).delete()
    return redirect('users:Profile', username=username)


def search_users(request):
    form = UserSearchForm()
    results = []
    if request.method == 'GET' and 'query' in request.GET:
        form = UserSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            user_list = User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
            paginator = Paginator(user_list, 10)  # 10 результатов на страницу
            page = request.GET.get('page')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
    return render(request, 'flatpages/Account123/search_results.html', {'form': form, 'results': results})
    
    
    
    
    
def license(request):
    return render(request, 'flatpages/main/html/license.html')
