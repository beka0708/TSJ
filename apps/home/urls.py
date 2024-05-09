from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('voice_recording/<int:vote_new_id>/', VotesListView.as_view(), name='vote_list'),
    path('votes/', VoteViewSet.as_view, name='vote'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HouseViewSet,
    FlatOwnerViewSet,
    FlatTenantViewSet,
    FlatViewSet,
    NewsOwnerViewSet,
    VoteViewSet,
    VotesListView,
    RequestVoteViewSet,
)

router = DefaultRouter()
router.register("house", HouseViewSet)
router.register("flat_owners", FlatOwnerViewSet)
router.register("flat_tenants", FlatTenantViewSet)
router.register("flats", FlatViewSet)
router.register("news_owners", NewsOwnerViewSet)
router.register(r"votes", VoteViewSet)
router.register(r"request_votes", RequestVoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("votes/<int:vote_id>/", VotesListView.as_view(), name="votes-list"),
]
