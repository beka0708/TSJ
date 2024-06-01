from django.urls import path
from .views import (
    UserRegistrationView,
    PhoneNumberAuthenticationView,
    DeviceTokenAPIView,
    VerifyCodeView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("login/", PhoneNumberAuthenticationView.as_view(), name="phone_number_login"),
    path("device_token/", DeviceTokenAPIView.as_view(), name="device-token"),
    path("code/", VerifyCodeView.as_view(), name="verify_code"),
]
