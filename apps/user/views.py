from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.hashers import make_password
from .backends import PhoneNumberBackend
from .models import DeviceToken
from .permissions import AllowAny
from .serializers import UserSerializer, DeviceTokenSerializer
from .utils import SendSMS
from rest_framework import status, views
from rest_framework.response import Response
from .models import CustomUser

CustomUser = get_user_model()


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Отправляем SMS с кодом подтверждения
            # SendSMS.send_confirmation_sms(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
############################################################################################33
#
#
# class VerifyCodeView(views.APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         phone_number = request.data.get("phone_number", None)
#         verification_code = request.data.get("verification_code", None)
#
#         if phone_number and verification_code:
#             try:
#                 user = CustomUser.objects.get(phone_number=phone_number)
#                 if user.verification_code == verification_code:
#                     user.is_approved = True
#                     user.save()
#                     return Response(
#                         {
#                             "message": "Код подтверждения верный. Можете установить новый пароль."
#                         },
#                         status=status.HTTP_200_OK,
#                     )
#                 else:
#                     return Response(
#                         {"error": "Неверный код подтверждения."},
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#             except CustomUser.DoesNotExist:
#                 return Response(
#                     {"error": "Пользователь с указанным номером телефона не найден."},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#         else:
#             return Response(
#                 {"error": "Необходимо указать номер телефона и код подтверждения."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#
# class SetNewPasswordView(views.APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         phone_number = request.data.get("phone_number")
#         verification_code = request.data.get("verification_code")
#         new_password = request.data.get("new_password")
#
#         if not all([phone_number, verification_code, new_password]):
#             return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             user = CustomUser.objects.get(phone_number=phone_number)
#             if user.verification_code == verification_code:
#                 # Обновляем пароль пользователя
#                 user.password = make_password(new_password)
#                 user.save()
#                 return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
