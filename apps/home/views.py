from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.views import APIView

from .serializers import *
from rest_framework import viewsets
from rest_framework import status
from .models import House, FlatOwner, FlatTenant, Flat, News, Request
from .serializers import (
    HouseSerializers, FlatOwnerSerializers, FlatTenantSerializers,
    FlatSerializers, NewsOwnerSerializers, RequestSerializers
)


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializers


class FlatOwnerViewSet(viewsets.ModelViewSet):
    queryset = FlatOwner.objects.all()
    serializer_class = FlatOwnerSerializers


class FlatTenantViewSet(viewsets.ModelViewSet):
    queryset = FlatTenant.objects.all()
    serializer_class = FlatTenantSerializers


class FlatViewSet(viewsets.ModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializers


class NewsOwnerViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsOwnerSerializers


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializers


from django.utils import timezone  # Import Django's timezone module

class VoteViewSet(viewsets.ModelViewSet):
    queryset = VoteNew.objects.all()
    serializer_class = VoteNewSerializer

    # permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Необходима аутентификация."}, status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()

        # Check if the deadline has passed
        if instance.deadline <= timezone.now():  # Use timezone.now() instead of datetime.now()
            return Response({"error": "Голосование уже завершено."}, status=status.HTTP_400_BAD_REQUEST)

        # проверка голосов пользователей
        user_has_voted = instance.votes.filter(user=request.user).exists()
        if user_has_voted:
            return Response({"error": "Вы уже проголосовали."}, status=status.HTTP_400_BAD_REQUEST)

        if 'vote' in request.data:
            vote_value = request.data['vote']
            if vote_value == 'за':
                instance.yes_count += 1
            elif vote_value == 'против':
                instance.no_count += 1
            instance.save()

            # чтобы не голосовали повторно
            instance.votes.create(user=request.user, vote=vote_value)

        return super().update(request, *args, **kwargs)
        #
        # total_votes = instance.yes_count + instance.no_count
        # if total_votes > 0:
        #     percentage_yes = (instance.yes_count / total_votes) * 100
        #     percentage_no = (instance.no_count / total_votes) * 100
        # else:
        #     percentage_yes = 0
        #     percentage_no = 0
        #
        # return Response({
        #     "percentage_yes": percentage_yes,
        #     "percentage_no": percentage_no
        # })


class VotesListView(APIView):
    def get(self, request, *args, **kwargs):
        vote_new_id = kwargs.get('vote_new_id')
        votes = Votes.objects.filter(vote_new_id=vote_new_id)
        serializer = VotesSerializer(votes, many=True)
        return Response(serializer.data)

