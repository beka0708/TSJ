from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HouseViewSet,
    # FlatOwnerViewSet,
    FlatTenantViewSet,
    FlatViewSet,

    ListDeadLineApiView,
    VoteViewSet,
    FeedHomeView,
    RequestVoteViewSet, ApartmentHistoryViewSet, ListTSJView
)

router = DefaultRouter()
router.register("house", HouseViewSet)
router.register(r"votes", VoteViewSet)
router.register(r"request_votes", RequestVoteViewSet)
router.register(r'apartment_history', ApartmentHistoryViewSet, basename="flat_history")

urlpatterns = [
    path("", include(router.urls)),
    path("feed/", FeedHomeView.as_view()),
    path("deadlines/", ListDeadLineApiView.as_view()),
    path("tsj/", ListTSJView.as_view()),
]
