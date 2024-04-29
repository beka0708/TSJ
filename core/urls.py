from django.contrib import admin
from django.urls import path, include
from apps.user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.home.urls')),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', PhoneNumberAuthenticationView.as_view(), name='phone_number_login'),
]
