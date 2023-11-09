from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post
from datetime import datetime
from .forms import RegisterForm

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from .forms import MessageForm

# Create your views here.
#@login_required(login_url='/login')
def home(request):
    date = request.GET.get('date')
    if date:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        posts = Post.objects.filter(date_created__date=date)
    else:
        posts = Post.objects.all()
    return render(request, 'main/home.html', {'posts': posts})



@login_required
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            description = request.POST.get('description')
            #author_username = request.POST.get('author')
            author = User.objects.get(username=request.user.username)
            post = Post.objects.create(title=title, description=description, author=author)
            post.save()
            return redirect('home')
    return render(request, 'main/create_post.html', {'form': form})


def search_posts(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            posts = Post.objects.filter(date_created__range=[start_date, end_date])

        else:
            posts = Post.objects.all()

        return render(request, 'main/home.html', {'posts': posts})  
    
    return render(request, 'main/home.html', {'posts': []})
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {"form": form})   


@login_required
def display_user(request):
    user = User.objects.get(username=request.user.username)  # Replace 'username' with the actual username
    return render(request, 'main/userprofile.html', {'user': user}) 





@login_required
def create_chat_room(request):
    if request.method == 'POST':
        chat_room_name = request.POST.get('chat_room_name')
        chat_room = ChatRoom.objects.create(name=chat_room_name)
    chat_room.users.add(request.user)
    chat_room.save()
    return render(request, 'chat/chat_room.html', {'chat_room': chat_room})

@login_required
def send_message(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.chat_room = chat_room
            message.save()
    return render(request, 'chat/chat_room.html', {'chat_room': chat_room})


@login_required
def fetch_messages(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    messages = Message.objects.filter(chat_room=chat_room).order_by('created_at')
    return render(request, 'chat/messages.html', {'messages': messages})