from rest_framework.response import Response
from .models import News, NewsView
from .serializers import NewsSerializer, CurrentNewsSerializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from apps.mixins.mixins import CreateGetListViewSet
from rest_framework import status
from rest_framework.decorators import action


class NewsViewSet(CreateGetListViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "description", ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
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

    @action(detail=False, methods=['get'])
    def get_my_news(self, request):
        user = request.user
        news = News.objects.filter(from_user_id=user.id)
        serializer = CurrentNewsSerializers(news, many=True, read_only=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# class NewsRequestsApiView()


def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context
