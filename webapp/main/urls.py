
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    # add more URL patterns here
    path('create_post/', views.create_post, name='create_post'),
   # path('home/', views.search_posts, name='search_posts'),
]