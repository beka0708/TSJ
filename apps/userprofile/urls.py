from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ChangePasswordViewSet, RequestViewSet

router = DefaultRouter()

router.register(r'profiles', ProfileViewSet, basename='profile')
# router.register(r'profiles', ProfileViewSet, basename='profile-list-create-retrieve-update')
router.register(r'change-password', ChangePasswordViewSet, basename='change-password')

urlpatterns = [
    path("", include(router.urls)),

]


