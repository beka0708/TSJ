from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DomKomViewSet, YourFormsViewSet, CameraViewSet, ReceiptsViewSet, HelpInfoViewSet

router = DefaultRouter()
router.register(r'domkom', DomKomViewSet)
router.register(r'yourforms', YourFormsViewSet)
router.register(r'camera', CameraViewSet)
router.register(r'receipts', ReceiptsViewSet)
router.register(r'helpinfo', HelpInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
