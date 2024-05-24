from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HouseViewSet,
    FlatOwnerViewSet,
    FlatTenantViewSet,
    FlatViewSet,
    NewsViewSet,
    VoteViewSet,
    RequestVoteViewSet, ApartmentHistoryViewSet,
)

router = DefaultRouter()
router.register("house", HouseViewSet)
router.register("flat_owners", FlatOwnerViewSet)
router.register("flat_tenants", FlatTenantViewSet)
router.register("flats", FlatViewSet)
router.register("news", NewsViewSet)
router.register(r"votes", VoteViewSet)
router.register(r"request_votes", RequestVoteViewSet)
router.register(r'apartment_history', ApartmentHistoryViewSet, basename="flat_history")

urlpatterns = [
    path("", include(router.urls)),
    # path("votes/<int:vote_id>/", VotesListView.as_view(), name="votes-list"),
]
