from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from apps.home.models import RequestVoteNews, House
from apps.home.serializers import RequestVoteSerializers
from .models import Camera, HelpInfo, Debt
from apps.mixins.mixins import RetrivListViewSet
from .serializers import (
    CameraSerializers,
    HelpInfoSerializers,
    DebtSerializer
)
from apps.home.serializers import HouseSerializers
from rest_framework.response import Response

User = get_user_model()


class GetMyHouseApiView(APIView):
    """
    Retriv current user House info.
    """
    serializer_class = HouseSerializers

    def get(self, request):
        user = request.user
        my_flat_list = user.flatowner_set.values_list('id')
        my_house = House.objects.filter(flat__id__in=my_flat_list)
        serializer = self.serializer_class(my_house, many=True, read_only=True)
        return Response(serializer.data)


class HistoryRequestViewSet(RetrivListViewSet):
    serializer_class = RequestVoteSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_requests = RequestVoteNews.objects.filter(user=user)
        return user_requests


class CameraViewSet(RetrivListViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializers


class HelpInfoViewSet(RetrivListViewSet):
    queryset = HelpInfo.objects.all()
    serializer_class = HelpInfoSerializers


class DebtViewSet(RetrivListViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
