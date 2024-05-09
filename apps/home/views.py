from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsManagerOrReadOnly
from .models import House, FlatOwner, FlatTenant, Flat, News
from .serializers import *
from .serializers import (
    HouseSerializers,
    FlatOwnerSerializers,
    FlatTenantSerializers,
    FlatSerializers,
    NewsOwnerSerializers,
)


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


class NewsOwnerViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsOwnerSerializers
    permission_classes = [IsManagerOrReadOnly]


class RequestVoteViewSet(viewsets.ModelViewSet):
    queryset = Request_Vote_News.objects.all()
    serializer_class = RequestVoteSerializers
    permission_classes = [IsOwnerOrReadOnly]


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Необходима аутентификация."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        instance = self.get_object()

        # Check if the deadline has passed
        if instance.deadline <= timezone.now():
            return Response(
                {"error": "Голосование уже завершено."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # проверка голосов пользователей
        user_has_voted = instance.votes.filter(user=request.user).exists()
        if user_has_voted:
            return Response(
                {"error": "Вы уже проголосовали."}, status=status.HTTP_400_BAD_REQUEST
            )

        if "vote" not in request.data:
            return Response(
                {
                    "error": "Пожалуйста, отправьте свой голос в формате JSON. "
                    "Например: {'vote': 'за'} или {'vote': 'против'}."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "vote" in request.data:
            vote_value = request.data["vote"]
            if vote_value == "за":
                instance.yes_count += 1
            elif vote_value == "против":
                instance.no_count += 1
            instance.save()

            # чтобы не голосовали повторно
            instance.votes.create(user=request.user, vote=vote_value)

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


class VotesListView(APIView):
    def get(self, request, *args, **kwargs):
        vote_id = kwargs.get("vote_id")
        votes = Votes.objects.filter(vote_new_id=vote_id)
        serializer = VotesSerializer(votes, many=True)
        return Response(serializer.data)
