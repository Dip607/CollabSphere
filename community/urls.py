from django.urls import path
from . import views

app_name = 'community'
# community/urls.py

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('my-mentor/', views.student_mentor_view, name='my_mentor'),
    path('my-students/', views.professor_student_list_view, name='my_students'),

    
    path('alumni-stories/', views.alumni_story_list, name='alumni_stories'),
    path('alumni-stories/new/', views.alumni_story_create, name='create_alumni_story'),
    
    
    # Direct Messaging URLs
    path('messages/', views.inbox, name='inbox'),
    path('messages/<int:user_id>/', views.conversation, name='conversation'),
    path('messages/<int:user_id>/send/', views.send_message, name='send_message'),
] 