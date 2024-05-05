from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TSJViewSet, HouseViewSet, FlatOwnerViewSet, FlatTenantViewSet, FlatViewSet,
    NewsViewSet, HelpInfoViewSet, VoteViewSet
)

router = DefaultRouter()
router.register(r'tsjs', TSJViewSet, basename='tsj')
router.register(r'houses', HouseViewSet, basename='house')
router.register(r'flatowners', FlatOwnerViewSet, basename='flatowner')
router.register(r'flattenants', FlatTenantViewSet, basename='flattenant')
router.register(r'flats', FlatViewSet, basename='flat')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'helpinfos', HelpInfoViewSet, basename='helpinfo')
router.register(r'votes', VoteViewSet, basename='vote')

urlpatterns = [
    path('', include(router.urls)),
]
