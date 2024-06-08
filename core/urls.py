from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from apps.chat.views import chat_room, room_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/home/", include("apps.home.urls")),
    path("api/auth/", include("apps.user.urls")),
    path("api/user/profile/", include("apps.userprofile.urls")),
    path("api/myhouse/", include("apps.my_house.urls")),
    path("api/chat/", include("apps.chat.urls")),
    path('api/rooms/', room_list, name='room_list'),
    path('chat/<int:room_id>/', chat_room, name='chat_room'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("api/blogs/", include('apps.blogs.urls')),
    path("api/payment/", include('apps.payment.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
