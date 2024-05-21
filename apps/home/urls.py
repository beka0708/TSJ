from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HouseViewSet,
    FlatOwnerViewSet,
    FlatTenantViewSet,
    FlatViewSet,
    VoteViewSet,
    VotesListView,
    RequestVoteViewSet, ApartmentHistoryViewSet, ViewRecordViewSet, NewsViewSet,
)

router = DefaultRouter()
router.register("house", HouseViewSet)
router.register("flat_owners", FlatOwnerViewSet)
router.register("flat_tenants", FlatTenantViewSet)
router.register("flats", FlatViewSet)
router.register(r"votes", VoteViewSet)  # голосование
router.register(r'view-records', ViewRecordViewSet, basename='view-record')  # все просмотры
router.register(r'news', NewsViewSet, basename='news')
router.register(r"request_votes", RequestVoteViewSet)
router.register(r'apartment_history', ApartmentHistoryViewSet, basename="flat_history")

urlpatterns = [
    path("", include(router.urls)),
    path("votes/<int:vote_id>/", VotesListView.as_view(), name="votes-list"),
]
