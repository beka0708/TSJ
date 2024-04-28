from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('sign-up/', views.UserCreateView.as_view()),
    path('sign-in/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('list/', views.UserListAPIView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
