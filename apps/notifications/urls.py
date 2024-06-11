from django.urls import path
from .views import ListNotificationsViews

urlpatterns = [
    path('', ListNotificationsViews.as_view())
]
