from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from apps.home.models import RequestVoteNews
from apps.home.serializers import RequestVoteSerializers
from .models import DomKom, Camera, HelpInfo, Debt

from .serializers import (
    DomKomSerializers, CameraSerializers,
    HelpInfoSerializers,
    DebtSerializer,
)


User = get_user_model()


class DomKomViewSet(viewsets.ModelViewSet):
    queryset = DomKom.objects.all()
    serializer_class = DomKomSerializers
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     user = self.request.user
    #     return DomKom.objects.filter(info=user)


class HistoryRequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestVoteSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_requests = Request_Vote_News.objects.filter(user=user)
        return user_requests


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializers


class HelpInfoViewSet(viewsets.ModelViewSet):
    queryset = HelpInfo.objects.all()
    serializer_class = HelpInfoSerializers


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
