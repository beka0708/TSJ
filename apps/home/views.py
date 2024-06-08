from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsManagerOrReadOnly
from itertools import chain
from .serializers import *
from .serializers import (
    HouseSerializers,
    FlatOwnerSerializers,
    FlatTenantSerializers,
    FlatSerializers,
)
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiParameter
from apps.payment.views import CsrfExemptSessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from apps.blogs.models import News
from django.db.models import Q


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
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "description", ]

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Необходима аутентификация."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        instance = self.get_object()

        if instance.deadline <= timezone.now():
            return Response(
                {"error": "Голосование уже завершено."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_has_voted = instance.votes.filter(user=request.user).exists()
        if user_has_voted:
            return Response(
                {"error": "Вы уже проголосовали."}, status=status.HTTP_400_BAD_REQUEST
            )

        vote_value = request.data.get('vote')
        if vote_value not in ['за', 'против']:
            return Response(
                {"error": "Пожалуйста, отправьте свой голос в формате JSON. "
                          "Например: {'vote': 'за'} или {'vote': 'против'}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if vote_value == "за":
            instance.yes_count += 1
        elif vote_value == "против":
            instance.no_count += 1
        instance.save()

        VoteResult.objects.create(vote=instance, user=request.user, vote_value=vote_value)

        total_votes = instance.yes_count + instance.no_count
        if total_votes > 0:
            percentage_yes = (instance.yes_count / total_votes) * 100
            percentage_no = (instance.no_count / total_votes) * 100
        else:
            percentage_yes = 0
            percentage_no = 0

        return Response(
            {"percentage_yes": percentage_yes, "percentage_no": percentage_no}
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_authenticated:
            VoteView.objects.get_or_create(vote=instance, user=request.user)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ApartmentHistoryViewSet(viewsets.ModelViewSet):
    queryset = ApartmentHistory.objects.all()
    serializer_class = ApartmentHistorySerializer


class FeedHomeView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='search',
                description='Search term for filtering results by title',
                required=False,
                type=str
            )
        ],
        responses={
            200: OpenApiResponse(
                response={
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'title': {'type': 'string'},
                            'desc': {'type': 'string'},
                            'type': {'type': 'string', 'enum': ['vote', 'news']},
                            'date_created': {'type': 'string', 'format': 'date-time'},
                            'vote_result': {
                                'type': 'object',
                                'properties': {
                                    'y': {'type': 'integer'},
                                    'n': {'type': 'integer'}
                                },
                                'nullable': True
                            },
                            'deadline': {'type': 'string', 'format': 'date-time', 'nullable': True}
                        },
                        'required': ['id', 'title', 'desc', 'type', 'date_created']
                    }
                },
                examples=[
                    OpenApiExample(
                        'Example Response',
                        summary='Detailed response',
                        value=[
                            {
                                'id': 1,
                                'title': 'Vote Title',
                                'desc': 'Vote Description',
                                'type': 'vote',
                                'date_created': '2022-01-01T00:00:00Z',
                                'vote_result': {'y': 10, 'n': 5},
                                'deadline': '2022-02-01T00:00:00Z',
                            },
                            {
                                'id': 2,
                                'title': 'News Title',
                                'desc': 'News Description',
                                'type': 'news',
                                'date_created': '2022-01-01T00:00:00Z',
                            },
                        ]
                    )
                ]
            )
        }
    )
    def get(self, request):
        search_query = request.query_params.get('search', None)
        vote_list = Vote.objects.all()
        news_list = News.objects.all()

        if search_query:
            vote_list = vote_list.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
            news_list = news_list.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        new_query = list(chain(vote_list, news_list))
        response = []

        for enti in new_query:
            new_enti = {
                'id': enti.id,
                'title': enti.title,
                'desc': enti.description,
                'type': 'vote' if isinstance(enti, Vote) else 'news',
                'date_created': enti.created_date,
            }
            if new_enti['type'] == 'vote':
                new_enti['vote_result'] = {'y': enti.yes_count, 'n': enti.no_count}
                new_enti['deadline'] = enti.deadline
            else:
                new_enti['vote_result'] = None
                new_enti['deadline'] = None
            response.append(new_enti)

        return Response(response)
