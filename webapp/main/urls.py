
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    # add more URL patterns here
    path('create_post/', views.create_post, name='create_post'),
   # path('home/', views.search_posts, name='search_posts'),
    path('display_user', views.display_user, name='display_user'),
    path('signup', views.signup, name='signup'),
    path('create_chat_room', views.create_chat_room, name='create_chat_room'),
    path('send_message/<int:chat_room_id>', views.send_message, name='send_message'),
    path('fetch_messages/<int:chat_room_id>', views.fetch_messages, name='fetch_messages'),

]