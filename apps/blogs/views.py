from rest_framework import viewsets
from rest_framework.response import Response
from .models import News, NewsView
from .serializers import NewsSerializer
from apps.home.permissions import IsManagerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "description", ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Учет просмотра пользователем
        if request.user.is_authenticated:
            NewsView.objects.get_or_create(news=instance, user=request.user)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
