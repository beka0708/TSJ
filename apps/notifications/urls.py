from django.urls import path
from .views import ListNotificationsViews, websocket_docs, test_page
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', ListNotificationsViews)

urlpatterns = [
    path('websocket-docs/', websocket_docs, name='websocket_docs'),
    path('websocket-test/', test_page, name='websocket_test')
]

urlpatterns += router.urls
