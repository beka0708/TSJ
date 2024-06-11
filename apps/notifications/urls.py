from django.urls import path
from .views import ListNotificationsViews,websocket_docs

urlpatterns = [
    path('websocket-docs/', websocket_docs, name='websocket_docs'),
    path('', ListNotificationsViews.as_view())
]
