from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from apps.chat.views import chat_room, room_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", include("apps.home.urls")),
    path("user/", include("apps.user.urls")),
    path("profile/", include("apps.userprofile.urls")),
    path("myhouse/", include("apps.my_house.urls")),
    path("chat/", include("apps.chat.urls")),
    path('rooms/', room_list, name='room_list'),
    path('chat/<str:room_name>/', chat_room, name='chat_room'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

]
if settings.DEBUG:
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'), ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
