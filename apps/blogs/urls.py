from rest_framework.routers import DefaultRouter
from .views import NewsViewSet
from django.urls import path

router = DefaultRouter()
router.register("news", NewsViewSet)


urlpatterns = router.urls
