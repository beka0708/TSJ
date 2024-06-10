from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HistoryRequestViewSet, CameraViewSet, \
    HelpInfoViewSet, \
    DebtViewSet, GetMyHouseApiView

router = DefaultRouter()
router.register(r'history', HistoryRequestViewSet, basename="your_forms")
router.register(r'camera', CameraViewSet, basename="camera")
router.register(r'help_info', HelpInfoViewSet, basename="help_info")
router.register(r'debt', DebtViewSet, basename="debt")

urlpatterns = [
    path('', include(router.urls)),
    path('current', GetMyHouseApiView.as_view()),
]
