from django.contrib import admin
from django.urls import path, include
from apps.user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/home/', include('apps.home.urls')),
    path('api/v1/user/', include('apps.user.urls')),
]
