from django.http import Http404

from .models import Profile, Request
from .serializers import ProfileSerializer, ChangePasswordSerializer, RequestSerializer
from rest_framework import status
from rest_framework.response import Response
from apps.home.permissions import IsManagerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets, mixins

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Profile
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        # Проверка, имеет ли пользователь доступ к этому профилю
        profile = self.get_object()
        if profile.user.id == request.user.id:
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        return Response({"detail": "У вас нет доступа к этому профилю."}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        # Обновление профиля пользователя
        profile = self.get_object()
        if profile.user.id == request.user.id:
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "У вас нет доступа к обновлению этого профиля."}, status=status.HTTP_403_FORBIDDEN)

    def get_object(self):
        # Получаем объект профиля по ID
        try:
            profile = Profile.objects.get(pk=self.kwargs.get('pk'))
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404


class ChangePasswordViewSet(viewsets.ModelViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Проверяем старый пароль
            if not self.object.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["Старый пароль неверен."]}, status=status.HTTP_400_BAD_REQUEST)
            # Устанавливаем новый пароль
            self.object.set_password(serializer.validated_data['new_password'])
            self.object.save()
            return Response({"status": "password set"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsManagerOrReadOnly]
