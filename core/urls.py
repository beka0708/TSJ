from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.home.views import *
from apps.home.views import *

router = DefaultRouter()
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/home/', include('apps.home.urls')),
    path('api/v1/user/', include('apps.user.urls')),
    path('api/v1/vote/', include('apps.home.urls'))

]





