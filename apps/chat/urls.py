from django.urls import path
from . import views

urlpatterns = [
    path('chats/', views.ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', views.ChatDetailView.as_view(), name='chat-detail'),
    path('chats/<int:chat_id>/messages/', views.MessageListCreateView.as_view(), name='message-list-create'),
]
