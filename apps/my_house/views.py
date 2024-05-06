from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import DomKom, YourForms, Camera, Receipts, HelpInfo
from .serializers import (
    DomKomSerializers, YourFormsSerializers, CameraSerializers,
    ReceiptsSerializers, HelpInfoSerializers
)


class DomKomViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DomKomSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return DomKom.objects.filter(info=user)


class YourFormsViewSet(viewsets.ModelViewSet):
    serializer_class = YourFormsSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return YourForms.objects.filter(user=user)


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
