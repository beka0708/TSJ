from rest_framework import viewsets
from .permissions import IsManagerOrOwnerOrTenant
from .serializers import (
    TSJSerializer, HouseSerializer, FlatSerializer, FlatOwnerSerializer, FlatTenantSerializer,
    NewsSerializer, RequestSerializer, HelpInfoSerializer, VoteSerializer
)
from .models import TSJ, House, FlatOwner, FlatTenant, Flat, News, Request, HelpInfo, Vote


class TSJViewSet(viewsets.ModelViewSet):
    queryset = TSJ.objects.all()
    serializer_class = TSJSerializer
    permission_classes = [IsManagerOrOwnerOrTenant]


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsManagerOrOwnerOrTenant]


class FlatOwnerViewSet(viewsets.ModelViewSet):
    queryset = FlatOwner.objects.all()
    serializer_class = FlatOwnerSerializer
    permission_classes = [IsManagerOrOwnerOrTenant]


class FlatTenantViewSet(viewsets.ModelViewSet):
    queryset = FlatTenant.objects.all()
    serializer_class = FlatTenantSerializer
    permission_classes = [IsManagerOrOwnerOrTenant]


class FlatViewSet(viewsets.ModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer
    permission_classes = [IsManagerOrOwnerOrTenant]


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsManagerOrOwnerOrTenant]


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsManagerOrOwnerOrTenant]


class HelpInfoViewSet(viewsets.ModelViewSet):
    queryset = HelpInfo.objects.all()
    serializer_class = HelpInfoSerializer
    permission_classes = [IsManagerOrOwnerOrTenant]


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsManagerOrOwnerOrTenant]
