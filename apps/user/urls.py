from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.UserListAPIView.as_view()),
    path('create/', views.UserCreateView.as_view()),
    path('profile/', views.ProfileView.as_view())
]
