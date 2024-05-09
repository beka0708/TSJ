from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.home.models import Request_Vote_News
from .models import DomKom, Camera, Receipts, HelpInfo
from .serializers import (
    DomKomSerializers, CameraSerializers,
    ReceiptsSerializers, HelpInfoSerializers
)
from apps.home.serializers import RequestVoteSerializers
from apps.userprofile.serializers import RequestSerializer


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


class ReceiptsViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptsSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Receipts.objects.filter(user=user)


class HelpInfoViewSet(viewsets.ModelViewSet):
    queryset = HelpInfo.objects.all()
    serializer_class = HelpInfoSerializers
