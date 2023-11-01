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
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'main/create_post.html', {'form': form})

'''
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
    '''