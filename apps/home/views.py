from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsManagerOrReadOnly
from .serializers import (
    HouseSerializers,
    FlatOwnerSerializers,
    FlatTenantSerializers,
    FlatSerializers,
    NewsOwnerSerializers,
    RequestVoteSerializers,
    VoteSerializer,
    ApartmentHistorySerializer,
    VotesSerializer,
    ViewRecordSerializer,
)
from ..user.serializers import UserSerializer
from .models import House, FlatOwner, FlatTenant, Flat, Request_Vote_News, Vote, News, ViewRecord, ApartmentHistory, \
    Votes, User
from django.utils.translation import get_language
from .models import TSJ


# def tsj_detail(request, tsj_id):
#     current_language = get_language()
#     tsj_instance = TSJ.objects.get(id=tsj_id)
#     context = {
#         'tsj': tsj_instance,
#         'current_language': current_language,
#     }
#     return render(request, 'tsj_detail.html', context)
#

class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializers
    permission_classes = [IsAdminOrReadOnly]


class FlatOwnerViewSet(viewsets.ModelViewSet):
    queryset = FlatOwner.objects.all()
    serializer_class = FlatOwnerSerializers
    permission_classes = [IsOwnerOrReadOnly]


class FlatTenantViewSet(viewsets.ModelViewSet):
    queryset = FlatTenant.objects.all()
    serializer_class = FlatTenantSerializers
    permission_classes = [IsOwnerOrReadOnly]


class FlatViewSet(viewsets.ModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializers
    permission_classes = [IsManagerOrReadOnly]


class RequestVoteViewSet(viewsets.ModelViewSet):
    queryset = Request_Vote_News.objects.all()
    serializer_class = RequestVoteSerializers
    permission_classes = [IsOwnerOrReadOnly]


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsManagerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_authenticated:
            view_record, created = ViewRecord.objects.get_or_create(
                user=request.user,
                content_type='vote',
                content_id=instance.id,
                defaults={'viewed_at': timezone.now()}
            )
            if created:
                instance.view_count += 1
                instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ApartmentHistoryViewSet(viewsets.ModelViewSet):
    queryset = ApartmentHistory.objects.all()
    serializer_class = ApartmentHistorySerializer


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'MANAGER'


class VotesListView(APIView):
    def get(self, request, *args, **kwargs):
        vote_id = kwargs.get("vote_id")
        votes = Votes.objects.filter(vote_new_id=vote_id)
        serializer = VotesSerializer(votes, many=True)
        return Response(serializer.data)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsOwnerSerializers
    permission_classes = [IsManagerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_authenticated:
            view_record, created = ViewRecord.objects.get_or_create(
                user=request.user,
                content_type='news',
                content_id=instance.id,
                defaults={'viewed_at': timezone.now()}
            )
            if created:
                instance.view_count += 1
                instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def viewers(self, request, pk=None):
        news = self.get_object()
        viewed_users = User.objects.filter(viewrecord__content_type='news', viewrecord__content_id=news.id)
        serializer = UserSerializer(viewed_users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def non_viewers(self, request, pk=None):
        news = self.get_object()
        all_users = User.objects.all()
        viewed_users = User.objects.filter(viewrecord__content_type='news', viewrecord__content_id=news.id)
        non_viewed_users = all_users.exclude(id__in=viewed_users)
        serializer = UserSerializer(non_viewed_users, many=True)
        return Response(serializer.data)


class ViewRecordViewSet(viewsets.ModelViewSet):
    queryset = ViewRecord.objects.all()
    serializer_class = ViewRecordSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type', None)
        queryset = ViewRecord.objects.all()
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        return queryset
