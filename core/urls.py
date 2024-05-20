from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.chat.views import index

urlpatterns = [
      path("admin/", admin.site.urls),
      path("home/", include("apps.home.urls")),
      path("user/", include("apps.user.urls")),
      path("profile/", include("apps.userprofile.urls")),
      path("myhouse/", include("apps.my_house.urls")),
      path("chat/", include("apps.chat.urls")),
      path('chat_index/', index, name='chat'),
      path("ckeditor5/", include('django_ckeditor_5.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
