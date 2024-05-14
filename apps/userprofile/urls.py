from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, ChangePasswordViewSet, RequestViewSet, \
    SendVerificationCodeViewSet, ChangeSendPasswordViewSet

router = DefaultRouter()

router.register(r'requests', RequestViewSet, basename='request')
router.register(r'profiles', ProfileViewSet, basename='profile-list-create-retrieve-update')
router.register(r'change-password', ChangePasswordViewSet, basename='change-password')
router.register(r'change-send-password', ChangeSendPasswordViewSet, basename='change-send-password')
router.register(r'send-code', SendVerificationCodeViewSet, basename='send-verification-code')

urlpatterns = [
    path("", include(router.urls)),
]
