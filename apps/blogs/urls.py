from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, test_page
from django.urls import path

router = DefaultRouter()
router.register("news", NewsViewSet)

urlpatterns = [path('test', test_page)]
urlpatterns += router.urls
