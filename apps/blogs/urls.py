from rest_framework.routers import DefaultRouter
from .views import NewsViewSet

router = DefaultRouter()
router.register("news", NewsViewSet)

urlpatterns = router.urls
