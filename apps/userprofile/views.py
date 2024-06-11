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
from apps.mixins.mixins import WithoutDeleteViewSet, RetrivUpdateViewSet
from django.http import Http404

User = get_user_model()


class ProfileViewSet(WithoutDeleteViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class CurrentProfileView(APIView):
    """
    A view for updating or retrieving the authenticated user's profile.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = self.serializer_class(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = self.serializer_class(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

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
                user.set_password(str(serializer.validated_data['new_password']))
                user.save()
                password_reset.used = True
                password_reset.save()
                return Response({'message': 'Password has been reset'}, status=status.HTTP_200_OK)
            except PasswordReset.DoesNotExist:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestViewSet(WithoutDeleteViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsManagerOrReadOnly]
