from .models import Notification
from .serializer import NotificationSerializer
from django.shortcuts import render
from apps.mixins.mixins import WithoutDeleteViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ListNotificationsViews(WithoutDeleteViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = self.queryset.filter(user_id=user_id)
        return queryset

    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response(status=status.HTTP_200_OK)


def websocket_docs(request):
    return render(request, 'websocket_docs.html')


def test_page(request):
    return render(request, 'noti.html')
