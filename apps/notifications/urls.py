from django.urls import path
from .views import ListNotificationsViews, websocket_docs, test_page

urlpatterns = [
    path('websocket-docs/', websocket_docs, name='websocket_docs'),
    path('websocket-test/', test_page, name='websocket_test'),
    path('', ListNotificationsViews.as_view())
]
