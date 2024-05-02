from rest_framework import generics
from .permissions import IsManager
from .serializers import (
    TSJSerializer, HouseSerializer, FlatSerializer, FlatOwnerSerializer, FlatTenantSerializer,
    NewsSerializer, RequestSerializer, HelpInfoSerializer, VoteSerializer
)
from .models import TSJ, House, FlatOwner, FlatTenant, Flat, News, Request, HelpInfo, Vote


class TSJListView(generics.ListAPIView):
    queryset = TSJ.objects.all()
    serializer_class = TSJSerializer


class TSJCreateView(generics.CreateAPIView):
    queryset = TSJ.objects.all()
    serializer_class = TSJSerializer
    permission_classes = [IsManager]


class TSJUpdateView(generics.UpdateAPIView):
    queryset = TSJ.objects.all()
    serializer_class = TSJSerializer
    permission_classes = [IsManager]


class TSJDestroyView(generics.DestroyAPIView):
    queryset = TSJ.objects.all()
    serializer_class = TSJSerializer
    permission_classes = [IsManager]


class HouseListView(generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer


class HouseCreateView(generics.CreateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsManager]


class HouseUpdateView(generics.UpdateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsManager]


class HouseDestroyView(generics.DestroyAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsManager]


class FlatOwnerListView(generics.ListAPIView):
    queryset = FlatOwner.objects.all()
    serializer_class = FlatOwnerSerializer


class FlatOwnerCreateView(generics.CreateAPIView):
    queryset = FlatOwner.objects.all()
    serializer_class = FlatOwnerSerializer
    permission_classes = [IsManager]


class FlatOwnerUpdateView(generics.UpdateAPIView):
    queryset = FlatOwner.objects.all()
    serializer_class = FlatOwnerSerializer
    permission_classes = [IsManager]


class FlatOwnerDestroyView(generics.DestroyAPIView):
    queryset = FlatOwner.objects.all()
    serializer_class = FlatOwnerSerializer
    permission_classes = [IsManager]


class FlatTenantListView(generics.ListAPIView):
    queryset = FlatTenant.objects.all()
    serializer_class = FlatTenantSerializer


class FlatTenantCreateView(generics.CreateAPIView):
    queryset = FlatTenant.objects.all()
    serializer_class = FlatTenantSerializer
    permission_classes = [IsManager]


class FlatTenantUpdateView(generics.UpdateAPIView):
    queryset = FlatTenant.objects.all()
    serializer_class = FlatTenantSerializer
    permission_classes = [IsManager]


class FlatTenantDestroyView(generics.DestroyAPIView):
    queryset = FlatTenant.objects.all()
    serializer_class = FlatTenantSerializer
    permission_classes = [IsManager]


class FlatListView(generics.ListAPIView):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer


class FlatCreateView(generics.CreateAPIView):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer
    permission_classes = [IsManager]


class FlatUpdateView(generics.UpdateAPIView):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer
    permission_classes = [IsManager]


class FlatDestroyView(generics.DestroyAPIView):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer
    permission_classes = [IsManager]


class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsCreateView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsManager]


class NewsUpdateView(generics.UpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsManager]


class NewsDestroyView(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsManager]


class RequestListView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class RequestCreateView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class RequestUpdateView(generics.UpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsManager]


class RequestDestroyView(generics.DestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsManager]


class HelpInfoListView(generics.ListAPIView):
    queryset = HelpInfo.objects.all()
    serializer_class = HelpInfoSerializer


class HelpInfoCreateView(generics.CreateAPIView):
    queryset = HelpInfo.objects.all()
    serializer_class = HelpInfoSerializer


class HelpInfoUpdateView(generics.UpdateAPIView):
    queryset = HelpInfo.objects.all()
    serializer_class = HelpInfoSerializer
    permission_classes = [IsManager]


class HelpInfoDestroyView(generics.DestroyAPIView):
    queryset = HelpInfo.objects.all()
    serializer_class = HelpInfoSerializer
    permission_classes = [IsManager]


class VoteListView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class VoteCreateView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsManager]


class VoteUpdateView(generics.UpdateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsManager]


class VoteDestroyView(generics.DestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsManager]
