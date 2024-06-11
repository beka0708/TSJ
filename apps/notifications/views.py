from rest_framework.generics import ListAPIView
from .models import Notification
from .serializer import NotificationSerializer
from django.shortcuts import render


class ListNotificationsViews(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = self.queryset.filter(user_id=user_id)
        return queryset


def websocket_docs(request):
    return render(request, 'websocket_docs.html')

def test_page(request):
    return render(request, 'noti.html')