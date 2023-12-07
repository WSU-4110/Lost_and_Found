
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_report, name='list_report'),
    path('home', views.home, name='home'),
    # add more URL patterns here
    path('create_post/', views.create_post, name='create_post'),
   # path('home/', views.search_posts, name='search_posts'),
    path('display_user', views.display_user, name='display_user'),
    path('signup', views.signup, name='signup'),
    path('otp_verification', views.otp_verification, name='otp_verification'),
    #path('create_chat_room', views.create_chat_room, name='create_chat_room'),
    #path('send_message/<int:chat_room_id>', views.send_message, name='send_message'),
    #path('fetch_messages/<int:chat_room_id>', views.fetch_messages, name='fetch_messages'),
    path('create_report/', views.create_report, name='create_report'),
    #path('create_report/report_form/', views.report_form, name='report_form'),
    
    path('list_report/', views.list_report, name='list_report'),
     path('list_resolved/', views.list_resolved, name='list_resolved'),
    #path('upload/', views.image_upload, name='upload'),
    path('delete_report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('resolve_report/<int:report_id>/', views.resolve_report, name='resolve_report'),
    path('personal_list', views.personal_list, name='personal_list'),
    path('add_comment/<int:report_id>/', views.add_comment, name='add_comment'),
    path('list_discussions', views.list_discussions, name='list_discussions'),
    # yuliyas
    path('discussion_page/<int:report_id>/', views.discussion_page, name='discussion_page'),

    #path('create_report/report_form', views.report_form, name='report_form'),

    #path('create_report/report form', views.report_form, name='report_form'),
    #path('resolve/', views.resolve, name='resolve'),
    #path('post/<int:post_id>/resolve/', views.toggle_resolve, name='toggle_resolve'),

]
