from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('voice_recording/<int:vote_new_id>/', VotesListView.as_view(), name='vote_list'),
    path('votes/', VoteViewSet.as_view, name='vote'),
]