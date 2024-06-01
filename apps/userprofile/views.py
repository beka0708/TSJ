from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.user.utils import SendSMS
from apps.home.permissions import IsManagerOrReadOnly
from .models import Profile, Request, ResidenceCertificate
from .serializers import ProfileSerializer, ChangePasswordSerializer, \
    RequestSerializer, ResidenceCertificateSerializer, ChangeSendPasswordSerializer

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class ChangePasswordViewSet(viewsets.ModelViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

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


class SendVerificationCodeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Проверяем, существует ли номер телефона пользователя
        if not request.user.phone_number:
            return Response({"error": "Номер телефона пользователя не найден."}, status=status.HTTP_400_BAD_REQUEST)
        # Отправка кода подтверждения
        # SendSMS.send_confirmation_sms(request.user)
        return Response({"status": "Код отправлен."}, status=status.HTTP_200_OK)


class ChangeSendPasswordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ChangeSendPasswordSerializer(data=request.data)

        if serializer.is_valid():
            verification_code = serializer.validated_data['verification_code']
            new_password = serializer.validated_data['new_password']

            # Проверка кода
            user = request.user
            if user.verification_code != verification_code:
                return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)

            # Изменение пароля
            user.set_password(new_password)
            user.save()
            return Response({"status": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsManagerOrReadOnly]

