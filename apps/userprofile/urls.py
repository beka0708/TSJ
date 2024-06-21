from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CurrentProfileView,
    RequestViewSet,
    SendVerificationCodeViewSet,
    ConfirmPasswordResetView,
    CodeConfirmView,
    SwitchCurrentApiView,
    DeleteAccountView
)

router = DefaultRouter()

router.register(r'requests', RequestViewSet, basename='request')

urlpatterns = [
    path("send-reset-pass-code/", SendVerificationCodeViewSet.as_view()),
    path("reset-password/", ConfirmPasswordResetView.as_view()),
    path("confirm-reset-password-code/", CodeConfirmView.as_view()),
    path("current/", CurrentProfileView.as_view()),
    path("current/switch/tsj/<int:pk>", SwitchCurrentApiView.as_view()),
    path("current/delete-account", DeleteAccountView.as_view()),
    path("", include(router.urls)),
]
