from django.urls import path, include
from .views import PaymentTypeViewSet, PaymentAPI, PaymentStatusAPIView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'payment-types', PaymentTypeViewSet, basename="payment-types")

urlpatterns = [
    path('', PaymentAPI.as_view(), name='payment'),
    path('status/<int:order_id>/', PaymentStatusAPIView.as_view(), name='payment_status'),
]
urlpatterns += router.urls
