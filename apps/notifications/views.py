from rest_framework.generics import ListAPIView
from .models import Notification
from .serializer import NotificationSerializer


class ListNotificationsViews(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = self.queryset.filter(user_id=user_id)
        return queryset
