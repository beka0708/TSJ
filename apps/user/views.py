from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .models import MyUser
from .serializers import ProfileSerializer, UserCreateSerializer, UserListSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserListSerializer


class UserCreateView(APIView):

    def get(self, request):
        users = MyUser.objects.all()

        serializer = UserCreateSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request):
        user = MyUser.objects.get(id=request.user.id)

        serializer = ProfileSerializer(user)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProfileSerializer()
    )
    def patch(self, request):
        user = MyUser.objects.get(id=request.user.id)
        serializer = ProfileSerializer(instance=user, data=request.data, partial=True,
                                       context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

