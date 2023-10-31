from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
# Create your views here.
def home(request):
    return render(request, 'main/home.html')

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

def display_user(request):
    user = User.objects.get(username='username')  # Replace 'username' with the actual username
    return render(request, 'main/userprofile.html', user=user)
