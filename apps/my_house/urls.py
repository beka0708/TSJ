from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DomKomViewSet, HistoryRequestViewSet, CameraViewSet, \
    HelpInfoViewSet, \
    DebtViewSet, PaymentTypeViewSet, PaymentAPI, PaymentStatusAPIView

router = DefaultRouter()
router.register(r'domKom', DomKomViewSet, basename="DomKom")
router.register(r'your_forms', HistoryRequestViewSet, basename="your_forms")
router.register(r'camera', CameraViewSet, basename="camera")
router.register(r'help_info', HelpInfoViewSet, basename="help_info")
router.register(r'debt', DebtViewSet, basename="debt")
router.register(r'payment-types', PaymentTypeViewSet, basename="payment-types")


urlpatterns = [
    path('', include(router.urls)),
    path('payment/', PaymentAPI.as_view(), name='payment'),
    path('payment/status/<int:order_id>/', PaymentStatusAPIView.as_view(), name='payment_status'),
]