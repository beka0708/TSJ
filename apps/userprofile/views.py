from .models import Profile, Request
from .serializers import ProfileSerializer, ChangePasswordSerializer, RequestSerializer
from rest_framework import status
from rest_framework.response import Response
from apps.home.permissions import IsManagerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets, mixins


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


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