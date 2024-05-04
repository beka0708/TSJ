from django.urls import path
from .views import ProfileList, ProfileDetail, ChangePasswordView

urlpatterns = [
    path('profiles/', ProfileList.as_view(), name='profile-list'),
    path('profiles/', ProfileDetail.as_view(), name='profile-detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
