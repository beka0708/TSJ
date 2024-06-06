from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .utils import SendSMS
from apps.user.models import PasswordReset
from apps.home.permissions import IsManagerOrReadOnly
from .models import Profile, Request, ResidenceCertificate
from .serializers import ProfileSerializer, ChangePasswordSerializer, \
    RequestSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer, ConfirmResetPassCodeSerializer
from rest_framework.views import APIView
import random
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema

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


class SendVerificationCodeViewSet(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=PasswordResetRequestSerializer,

    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(phone_number=serializer.validated_data['phone_number'])
                password_reset, created = PasswordReset.objects.get_or_create(user=user, used=False)
                if not created:
                    password_reset.token = str(random.randint(1000, 9999))
                    password_reset.created_at = timezone.now()
                    password_reset.save()

                SendSMS.send_password_sms(user, password_reset.token)
                return Response({'message': 'Password reset token sent'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeConfirmView(APIView):
    @extend_schema(
        request=ConfirmResetPassCodeSerializer,

    )
    def post(self, request):
        serializer = ConfirmResetPassCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = PasswordReset.objects.filter(user__phone_number=serializer.validated_data['phone_number'],
                                                token=serializer.validated_data['code'],
                                                used=False
                                                ).first()
            if code:
                code.is_verif = True
                code.save()
                return Response({"success": True})
        return Response({"success": False})


class ConfirmPasswordResetView(APIView):
    @extend_schema(
        request=PasswordResetConfirmSerializer,

    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                password_reset = PasswordReset.objects.get(
                    token=serializer.validated_data['code'],
                    used=False,
                    created_at__gte=timezone.now() - timedelta(hours=24),
                    is_verif=True
                )
                user = password_reset.user
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                password_reset.used = True
                password_reset.save()
                return Response({'message': 'Password has been reset'}, status=status.HTTP_200_OK)
            except PasswordReset.DoesNotExist:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsManagerOrReadOnly]
