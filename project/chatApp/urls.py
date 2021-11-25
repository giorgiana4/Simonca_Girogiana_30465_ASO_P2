from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('chatBox/', views.chatBox_view, name='chatBoxe'),
    path('chat_group/', views.chat_view_groups, name='chat_groups'),
    # path('logout/', logout, {'next_page': 'login'}, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('chatBox/<int:sender>/<int:receiver>/', views.message_view, name='chatBox'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    # path('api/typing/<int:sender>/<int:receiver>/', views.typing_view, name='typing_action'),
    path('api/messages/', views.message_list, name='message-list'),
    path('create-group/', views.createGroup_view, name='create-group'),
]
