from django.urls import path
from .views import (
    UserRegistrationView,
    PhoneNumberAuthenticationView,
    DeviceTokenAPIView,
    VerifyCodeView,

)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path("login/", PhoneNumberAuthenticationView.as_view(), name="phone_number_login"),
    path("device_token/", DeviceTokenAPIView.as_view(), name="device-token"),
    path("code/", VerifyCodeView.as_view(), name="verify_code"),

]
