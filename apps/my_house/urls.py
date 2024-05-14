from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DomKomViewSet, HistoryRequestViewSet, CameraViewSet, \
    ReceiptsViewSet, HelpInfoViewSet, PaymentViewSet,\
    PaymentTypeViewSet, DebtViewSet

router = DefaultRouter()
router.register(r'domKom', DomKomViewSet, basename="DomKom")
router.register(r'your_forms', HistoryRequestViewSet, basename="your_forms")
router.register(r'camera', CameraViewSet, basename="camera")
router.register(r'receipts', ReceiptsViewSet, basename="receipts")
router.register(r'help_info', HelpInfoViewSet, basename="help_info")
router.register(r'payments', PaymentViewSet, basename="payments")

router.register(r'payment_type', PaymentTypeViewSet, basename="payment_type")
router.register(r'debt', DebtViewSet, basename="debt")

urlpatterns = [
    path('', include(router.urls)),
]