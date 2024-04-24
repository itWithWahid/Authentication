from django.urls import path
from . import views

urlpatterns = [
    path('ballot/<int:id>/',views.ballot,name="ballot" ),
    path('ballot_2/<int:id>/',views.ballot_2,name="ballot_2" ),
    path('vote_count_1/<int:id>/',views.vote_count_1,name="vote_count_1"),
    path('vote_count_2/<int:id>/',views.vote_count_2,name="vote_count_2"),
]