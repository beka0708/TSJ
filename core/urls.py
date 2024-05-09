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





from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", include("apps.home.urls")),
    path("user/", include("apps.user.urls")),
    path("profile/", include("apps.userprofile.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
