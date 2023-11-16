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
import random
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from .forms import MessageForm
from django.core.mail import send_mail
from datetime import datetime, timedelta

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
            user = form.save(commit=False)  # Don't save the user yet
            otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
            request.session['otp'] = otp  # Store the OTP in the session
            request.session['username'] = form.cleaned_data.get('username')
            request.session['email'] = form.cleaned_data.get('email')
            request.session['password'] = form.cleaned_data.get('password1')
            request.session['otp_time'] = str(datetime.now())  # Store the current time
            send_mail(
                'Your OTP',
                f'Your OTP is {otp}',
                'lostfoundwayne@gmail.com',
                [form.cleaned_data.get('email')],
                fail_silently=False,
            )
            return redirect('otp_verification')  # Redirect to OTP verification view
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})


def otp_verification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_time = datetime.strptime(request.session.get('otp_time'), '%Y-%m-%d %H:%M:%S.%f')
        if datetime.now() - otp_time > timedelta(minutes=2):  # Check if more than 2 minutes have passed
            messages.error(request, 'OTP expired')
        elif otp == str(request.session.get('otp')):
            User.objects.create_user(
                username=request.session.get('username'),
                email=request.session.get('email'),
                password=request.session.get('password')
            )
            messages.success(request, 'User created successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'registration/otp_verification.html')


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
