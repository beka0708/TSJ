from rest_framework.response import Response
from .models import News, NewsView
from .serializers import NewsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from apps.mixins.mixins import CreateGetListViewSet
from django.shortcuts import render
from rest_framework import status


class NewsViewSet(CreateGetListViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "description", ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user_id': request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Учет просмотра пользователем
        if request.user.is_authenticated:
            NewsView.objects.get_or_create(news=instance, user=request.user)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# class NewsRequestsApiView()



