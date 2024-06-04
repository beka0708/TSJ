from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .backends import PhoneNumberBackend
from .models import DeviceToken
from .permissions import AllowAny
from .serializers import UserSerializer, DeviceTokenSerializer
from .utils import SendSMS
from ..my_house.views import CsrfExemptSessionAuthentication

CustomUser = get_user_model()


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Отправляем SMS с кодом подтверждения
            SendSMS.send_confirmation_sms(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)  # Выводим ошибки валидации для отладки
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneNumberAuthenticationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get("phone_number", None)
        password = request.data.get("password", None)

        if phone_number and password:
            user = PhoneNumberBackend.authenticate(
                self, request=request, phone_number=phone_number, password=password
            )
            if user:
                if user.is_active and user.is_approved:
                    refresh = RefreshToken.for_user(user)
                    access_token = AccessToken.for_user(user)
                    return Response(
                        {
                            "refresh": str(refresh),
                            "access": str(access_token),
                        }
                    )
                else:
                    return Response(
                        {"error": "Пользователь не активирован или не одобрен."},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                return Response(
                    {"error": "Неверный номер телефона или пароль"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"error": "Требуются и номер телефона, и пароль"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeviceTokenAPIView(generics.CreateAPIView):
    queryset = DeviceToken.objects.all()
    serializer_class = DeviceTokenSerializer


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication,)

    def post(self, request):
        phone_number = request.data.get("phone_number", None)
        verification_code = request.data.get("verification_code", None)

        if phone_number and verification_code:
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
                if user.verification_code == verification_code:
                    user.is_approved = True
                    user.save()
                    return Response(
                        {
                            "message": "Код подтверждения верный. Регистрация успешно завершена."
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "Неверный код подтверждения."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "Пользователь с указанным номером телефона не найден."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": "Необходимо указать номер телефона и код подтверждения."},
                status=status.HTTP_400_BAD_REQUEST,
            )
