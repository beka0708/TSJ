from django.urls import path
from .views import (
    TSJListView, HouseListView, FlatOwnerListView, FlatTenantListView, FlatListView,
    NewsListView, RequestListView, HelpInfoListView, VoteListView,
    TSJCreateView, HouseCreateView, FlatOwnerCreateView, FlatTenantCreateView,
    FlatCreateView, NewsCreateView, RequestCreateView, HelpInfoCreateView, VoteCreateView
)

urlpatterns = [
    path('tsj/list', TSJListView.as_view(), name='tsj-list'),
    path('tsj/create/', TSJCreateView.as_view(), name='create-tsj'),
    path('houses/list', HouseListView.as_view(), name='house-list'),
    path('house/create/', HouseCreateView.as_view(), name='create-house'),
    path('flat-owners/list', FlatOwnerListView.as_view(), name='flat-owner-list'),
    path('flat-owner/create/', FlatOwnerCreateView.as_view(), name='create-flat-owner'),
    path('flat-tenants/list', FlatTenantListView.as_view(), name='flat-tenant-list'),
    path('flat-tenant/create/', FlatTenantCreateView.as_view(), name='create-flat-tenant'),
    path('flats/list', FlatListView.as_view(), name='flat-list'),
    path('flat/create/', FlatCreateView.as_view(), name='create-flat'),
    path('news/list', NewsListView.as_view(), name='news-list'),
    path('news/create/', NewsCreateView.as_view(), name='create-news'),
    path('requests/list', RequestListView.as_view(), name='request-list'),
    path('request/create/', RequestCreateView.as_view(), name='create-request'),
    path('help-info/list', HelpInfoListView.as_view(), name='help-info-list'),
    path('help-info/create/', HelpInfoCreateView.as_view(), name='create-help-info'),
    path('votes/list', VoteListView.as_view(), name='vote-list'),
    path('vote/create/', VoteCreateView.as_view(), name='create-vote'),
]
