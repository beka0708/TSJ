from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, RequestViewSet, \
    SendVerificationCodeViewSet, ConfirmPasswordResetView, CodeConfirmView

router = DefaultRouter()

router.register(r'requests', RequestViewSet, basename='request')
router.register(r'', ProfileViewSet, basename='profile-list-create-retrieve-update')


urlpatterns = [
    path("send-reset-pass-code/", SendVerificationCodeViewSet.as_view()),
    path("reset-password/", ConfirmPasswordResetView.as_view()),
    path("confirm-reset-password-code/", CodeConfirmView.as_view()),
    path("", include(router.urls)),
]
