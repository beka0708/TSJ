from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = Profile.objects.get(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        if not user.check_password(data.get('old_password')):
            return Response({'old_password': ['Неверный пароль.']}, status=status.HTTP_400_BAD_REQUEST)

        if data.get('new_password') != data.get('confirm_new_password'):
            return Response({'confirm_new_password': ['Новые пароли не совпадают.']},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(data.get('new_password'))
        user.save()

        return Response({'detail': 'Пароль успешно изменен.'})
