from django.urls import path
from .views import UserRegistrationView, PhoneNumberAuthenticationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', PhoneNumberAuthenticationView.as_view(), name='phone_number_login'),
]