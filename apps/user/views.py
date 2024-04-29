from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# from django.contrib.auth import authenticate
from .backends import PhoneNumberBackend


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneNumberAuthenticationView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number', None)
        password = request.data.get('password', None)

        if phone_number and password:
            user = PhoneNumberBackend.authenticate(self, request=request, phone_number=phone_number, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = AccessToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(access_token),
                })
            else:
                return Response({'error': 'Неверный номер телефона или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Требуются и номер телефона, и пароль'},
                            status=status.HTTP_400_BAD_REQUEST)
