
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('signup/', views.signup, name='signup'),

    # add more URL patterns here
]