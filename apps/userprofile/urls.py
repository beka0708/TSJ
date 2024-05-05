from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ChangePasswordViewSet, RequestViewSet

router = DefaultRouter()
router.register(r'requests', RequestViewSet, basename='request')
router.register(r'profiles', ProfileViewSet, basename='profile-list-create-retrieve-update')
router.register(r'change-password', ChangePasswordViewSet, basename='change-password')

urlpatterns = [
    path("", include(router.urls)),
    path("profiles/<int:id>/", ProfileViewSet.as_view({
        'get': 'list',
    }))
]
