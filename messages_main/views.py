import json

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request, HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView

from groups.models import PostForGroups
from .forms import *
from .models import *
from django.forms import ModelForm
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.models import User

from .tasks import send_email_task
# Create your views here.
from users.models import Block, FriendshipRequest
from channels.generic.websocket import AsyncWebsocketConsumer

from rest_framework.views import APIView
from rest_framework.response import Response
from flask import Flask, request, jsonify


def index(request):
    return HttpResponse('Страница приложения чата')





class DialogsView(View):
    def get(self, request):
        dialogs = Chat.objects.filter(members__in=[request.user.id])[:20]
        chats = Chat.objects.filter(type='C')
        users = User.objects.all()
        return render(request, 'flatpages/message/html/Messages.html', {'user_profile': request.user,
                                                                        'dialogs': dialogs, 'users': users,
                                                                        'chats': chats,
                                                                        })
                                                                        
                                                                        
                                                                        
                                                                        

    

    
    
    
    
    
    
class ChatListView(ListView):
    model = Chat
    template_name = 'flatpages/message/html/Messages.html'
    context_object_name = 'chats'

    def get_queryset(self):
        queryset = Chat.objects.filter(members=self.request.user)
        chat_type = self.request.GET.get('type')
        if chat_type in ['D', 'C']:
            queryset = queryset.filter(type=chat_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_type'] = self.request.GET.get('type', 'all')
        return context


@method_decorator(login_required, name='dispatch')
class ChatDetailView(DetailView):
    model = Chat
    template_name = 'flatpages/message/html/StartDialog.html'
    context_object_name = 'chat123'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.get_object()
        user = self.request.user
        
        # Check if the current user is blocked by any member or has blocked any member
        is_blocked = any(self.is_blocked(user, member) for member in chat.members.all())
        is_blocked_by_recipient = any(self.is_blocked(member, user) for member in chat.members.all())

        context.update({
            'Messageform123': MessageForm1234(),
            'is_blocked123': is_blocked,
            'is_blocked_by_recipient123': is_blocked_by_recipient,
            'chat_type': chat.type,  # передаем тип чата в контекст
        })
        return context

    def post(self, request, *args, **kwargs):
        chat = self.get_object()
        message_form = MessageForm1234(request.POST, request.FILES)
        
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.chat = chat
            message.author = request.user
            message.save()
            if chat.type == Chat.DIALOG:
                recipient = chat.members.exclude(id=request.user.id).first()
                message.save()  # Сначала сохраняем сообщение
                message.recipients.add(recipient)
            elif chat.type == Chat.CHAT:
                message.save()  # Сначала сохраняем сообщение
                for member in chat.members.all():
                    if member != request.user:
                        message.recipients.add(member)

            
            return redirect('messages_main:chat_detail', pk=chat.pk)
        return self.get(request, *args, **kwargs)

    @staticmethod
    def is_blocked(blocker, blocked):
        return Block.objects.filter(blocker=blocker, blocked=blocked).exists()


class ChatCreateView(CreateView):
    model = Chat
    form_class = ChatForm
    template_name = 'flatpages/message/html/chat_form.html'
    success_url = reverse_lazy('messages_main:dialogs')

    def form_valid(self, form):
        chat = form.save(commit=False)
        chat.save()
        chat.members.add(self.request.user)
        form.save_m2m()
        return super().form_valid(form)


class CreateDialogView(View):

    def get(self, request, chat_id, username):
        recipient = get_object_or_404(User, username=username)
        is_blocked = self.is_blocked(request.user, recipient)
        form = MessageForm1234()

        # Проверка на существование чатов с точно двумя участниками и типом DIALOG
        # chats = Chat.objects.filter(members__in=[request.user.id], type=Chat.DIALOG).annotate(
        #     c=Count('members')).filter(c=2, members__in=[recipient.id])
        #
        # chat = chats.first() if chats.exists() else None
        dialogs = Chat.objects.filter(
            type=Chat.DIALOG,
            members=request.user
        ).filter(
            members=recipient
        ).distinct()

        if dialogs.exists():
            dialog = dialogs.first()
            return redirect(
                reverse('messages_main:messages', kwargs={'dialogs_id': dialog.id, 'username': user.username}))
        else:
            # Создаем новый чат, если он не существует
            dialog = Chat.objects.create(type=Chat.DIALOG)
            dialogs.members.add(request.user)
            dialogs.members.add(recipient)
            dialogs.save()
            # Перенаправляем на новый чат
        return render(
            request,
            'flatpages/message/html/StartDialog.html',
            {
                'user_profile': request.user,
                'chat': dialog,
                'Messageform': form,
                'dialog_id': dialogs.id if dialogs else None,
                'recipients': recipient,
                'is_blocked': is_blocked
            }
        )

    def post(self, request, chat_id, username):
        form = MessageForm1234(request.POST, request.FILES)

        sender = request.user
        recipient = get_object_or_404(User, username=username)

        if self.is_blocked(sender, recipient):
            return HttpResponseForbidden("Вы не можете отправлять сообщения этому пользователю.")

        if self.is_blocked(recipient, sender):
            return HttpResponseForbidden("Этот пользователь заблокировал вас, вы не можете отправить ему сообщение.")

        if form.is_valid():
            message = form.save(commit=False)
            dialogs = get_object_or_404(Chat, id=chat_id)
            message.chat = dialogs
            message.author = sender
            message.recipient = recipient
            message.save()
            return redirect(
                reverse('messages_main:messages', kwargs={'chat_id': dialogs.id, 'message_id': message.id,'username': recipient.username}))

        # Проверка на существование чатов с точно двумя участниками и типом DIALOG
        dialog = Chat.objects.filter(
            type=Chat.DIALOG,
            members=request.user
        ).filter(
            members=recipient
        ).distinct()

        if dialog.exists():
            dialogs = dialog.first()
            return redirect(
                reverse('messages_main:messages', kwargs={'chat_id': dialogs.id, 'message_id': message.id,'username': recipient.username}))
        else:
            # Создаем новый чат, если он не существует
            dialog = Chat.objects.create(type=Chat.DIALOG)
            dialog.members.add(request.user)
            dialog.members.add(recipient)
            dialog.save()
            # Перенаправляем на новый чат

        return render(
            request,
            'flatpages/message/html/StartDialog.html',
            {
                'user_profile': request.user,
                'dialog': dialog,
                'Messageform': form,
                'dialog_id': dialog.id if dialog else None,
                'recipients': recipient,
                'is_blocked': self.is_blocked(request.user, recipient)
            }
        )

    @staticmethod
    def is_blocked(sender, recipient):
        return Block.objects.filter(blocker=sender, blocked=recipient).exists()


class MessagesView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, chat_id, message_id, username):
        chat = get_object_or_404(Chat, id=chat_id)
        sender = request.user
        recipient = get_object_or_404(User, username=username)
        photo = Message.photoForMessages
        if self.is_blocked(sender, recipient):
            return HttpResponseForbidden("Вы не можете отправлять сообщения этому пользователю.")
        elif self.is_blocked(recipient, sender):
            return HttpResponseForbidden("Этот пользователь заблокировал вас, вы не можете отправить ему сообщение.")
        else:
            message_form = MessageForm1234()
            is_blocked = self.is_blocked(request.user, recipient)

            # Fetch the message using message_id
            message = get_object_or_404(Message, id=message_id)

        return render(
            request,
            'flatpages/message/html/StartDialog.html',
            {
                'photoForMessage':photo,
                'user_profile123': request.user,
                'chat123': chat,
                'Messageform123': message_form,
                'chat_id123': chat_id,
                'recipients': recipient,
                'is_blocked123': is_blocked,
                'message': message
            }
        )

    def post(self, request, chat_id, message_id, username):
        if request.headers.get('Content-Type') == 'application/json':
            # Handle marking messages as read
            return self.mark_messages_as_read(request)
        else:
            # Handle sending a new message
            return self.send_message(request, chat_id, username)

    def send_message(self, request, chat_id, username):
        form = MessageForm1234
        sender = request.user
        recipient = get_object_or_404(User, username=username)
        photo = Message.photoForMessages
        if self.is_blocked(sender, recipient):
            return HttpResponseForbidden("Вы не можете отправлять сообщения этому пользователю.")
        elif self.is_blocked(recipient, sender):
            return HttpResponseForbidden("Этот пользователь заблокировал вас, вы не можете отправить ему сообщение.")
        else:
            if request.method == "POST":
                form = MessageForm1234(data=request.POST, files=request.FILES)
                if form.is_valid():
                    message = form.save(commit=False)
                    message.chat = get_object_or_404(Chat, id=chat_id)
                    message.author = sender
                    message.recipient = recipient
                    message.photo = request.FILES['photoForMessages']
                    message.save()
                    return JsonResponse({'success':True, 'message_id':message.id})

                chat = get_object_or_404(Chat, id=chat_id)
            return render(
                    request,
                    'flatpages/message/html/StartDialog.html',
                    {   
                        'photoForMessage':message.photoForMessages,
                        'user_profile123': request.user,
                        'chat123': chat,
                        'Messageform123': form,
                        'chat_id123': chat_id,
                        'recipients': recipient,
                        'is_blocked123': self.is_blocked(request.user, recipient)
                    }
                )
    @staticmethod
    def is_blocked(blocker, blocked):
        return Block.objects.filter(blocker=blocker, blocked=blocked).exists()


@csrf_exempt
@login_required
def mark_as_read(request, message_id):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=message_id)
        if request.user != message.author:
            message.is_readed = True
            message.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
# @csrf_exempt
# @login_required
# def mark_as_read(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         message_ids = data.get('message_ids', [])
#         messages = Message.objects.filter(id__in=message_ids, recipients=request.user)
#         for message in messages:
#             message.is_read = True
#             message.save()
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'failed'}, status=400)


def chat_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            chat = GlobalChat.objects.create(content=content, author_GC=request.user)
        chats = GlobalChat.objects.order_by('-pub_date')[:50]
        return render(request, 'flatpages/main/html/main.html', {'chats': chats})
    elif request.method == 'GET':
        content = request.POST.get('content')
        if content:
            chat = GlobalChat.objects.create(content=content, author_GC=request.user)
        chats = GlobalChat.objects.order_by('-pub_date')[:50]
        return render(request, 'flatpages/main/html/main.html', {'chats': chats})
    else:
        content = request.POST.get('content')
        if content:
            chat = GlobalChat.objects.create(content=content, author_GC=request.user)
        chats = GlobalChat.objects.order_by('-pub_date')[:50]
        return render(request, 'flatpages/main/html/main.html', {'chats': chats})

# send_email_task.delay('Subject','Message', ['rikudo.sanin98@mail.ru'])
@login_required
@csrf_exempt
def send_message(request):
    if request.method == 'POST':  
        try:
            chat_id = request.POST.get('chat_id')
            content = request.POST.get('message')
            
            if not chat_id or not content:
                return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
                
            chat = get_object_or_404(Chat, id=chat_id)
            message = Message.objects.create(chat=chat, author=request.user, message=content)
            
            return JsonResponse({'success': True, 'message_id': message.id})
            
        except Chat.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Chat not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
        
        
        
        
        
        
def get_messages(request, chat_id, message_id, username):
    try:
        # Здесь вы можете использовать chat_id и другие параметры для получения сообщений
        chat = Chat.objects.get(id=chat_id)
        messages = chat.message_set.all().values('author__username', 'message', 'pub_date')
        return JsonResponse(list(messages), safe=False)
    except Chat.DoesNotExist:
        raise Http404("Chat not found")

 
        
        
        
def chat_list(request):
   Dialog_chats = Chat.objects.filter(members=request.user.id, type='D')
   Group_chats = Chat.objects.filter(members=request.user.id, type='C')
   
   chat_data = []
   
   for chat in Dialog_chats:
       messages = chat.message_set.all()
       recipient =chat.members.exclude(id=request.user.id).first()
       chat_data.append({
           'id': chat.id,
           'type': 'D',
           'name': recipient,
           
           'messages': [{'author': msg.author.username, 'content': msg.message, 'pub_date': msg.pub_date, 'id': msg.id} for msg in messages],
       })
               
   for chat in Group_chats:
       messages = chat.message_set.all()
       chat_data.append({
           'id': chat.id,
           'type': 'C',
           'name': chat.name,
           'messages': [{'author': msg.author.username, 'content': msg.message, 'pub_date': msg.pub_date} for msg in messages],
       })
               
   return render(request, 'flatpages/message/html/FewChats.html', {
       'chat_data': chat_data,
       'user': request.user,
       'form':MessageForm1234(),
   })
# Добавьте новый метод для отправки сообщений через API





def send_message_api():
    chat_ids = request.form.getlist('chat_ids[]')  # Получаем список ID чатов
    content = request.form.get('content')  # Получаем содержимое сообщения

    if content:
        for chat_id in chat_ids:
            try:
                chat = Chat.query.get(chat_id)  # Получаем чат по ID
                if chat:
                    message = Message(chat_id=chat.id, author=request.user, content=content)  # Создаем сообщение
                    db.session.add(message)  # Добавляем сообщение в сессию
                    db.session.commit()  # Сохраняем изменения
                else:
                    continue  # Игнорируем, если чат не найден
            except Exception as e:
                print(f"Ошибка при сохранении сообщения: {e}")  # Логируем ошибку

        return jsonify({'status': 'success', 'message': 'Сообщения отправлены!'})
    
    return jsonify({'status': 'error', 'message': 'Содержимое сообщения не может быть пустым.'}), 400


    
    

@login_required
def get_multiple_chats(request):
    if request.method == 'POST':
        chat_ids = request.POST.getlist('chat_ids[]')
        chats_data = []
        
        for chat_id in chat_ids:
            try:
                chat = Chat.objects.get(id=chat_id, participants=request.user)
                messages = Message.objects.filter(chat=chat).order_by('-timestamp')[:50]
                
                chat_data = {
                    'chat_id': chat.id,
                    'name': chat.name or f"Чат {chat.id}",
                    'messages': [{
                        'id': msg.id,
                        'content': msg.content,
                        'sender': msg.sender.username,
                        'is_own': msg.sender == request.user,
                        'timestamp': msg.timestamp.strftime('%H:%M %d.%m.%Y')
                    } for msg in reversed(messages)]
                }
                chats_data.append(chat_data)
            except Chat.DoesNotExist:
                continue
                
        return JsonResponse({'chats': chats_data})
    return JsonResponse({'error': 'Invalid request'}, status=400)      
    
    
@login_required
def send_message_to_multiple_chats(request):
    if request.method == 'POST':
        chat_ids = request.POST.getlist('chat_ids[]')  # Получаем список ID чатов
        content = request.POST.get('content')  # Получаем содержимое сообщения

        if content:
            for chat_id in chat_ids:
                try:
                    chat = Chat.objects.get(id=chat_id)
                    message = Message.objects.create(chat=chat, author=request.user, content=content)
                    # Здесь можно добавить логику для уведомления участников чата о новом сообщении
                except Chat.DoesNotExist:
                    continue  # Игнорируем, если чат не найден

            return JsonResponse({'status': 'success', 'message': 'Сообщения отправлены!'})
        return JsonResponse({'status': 'error', 'message': 'Содержимое сообщения не может быть пустым.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Неверный запрос.'}, status=400)
    
    


class LastMessageView(APIView):
    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        last_message = chat.last_message()
        return Response({'last_message_id': last_message.id if last_message else None})

