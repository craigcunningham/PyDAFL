from django.urls import path
from django.urls import re_path as url
from dal import autocomplete
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from DAFLDraft import views, forms
from DAFLDraft.models import Player

urlpatterns = [
    path("", views.home, name="home"),
    path("DAFLDraft/<name>", views.hello_there, name="hello_there"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    # path("<slug:id>/", PlayerDetailView.as_view(), name="player-detail"),
    path("players/", views.PlayerListView.as_view(), name="player-list"),
    path("players/add/", views.PlayerCreateView.as_view(), name="player-add"),
    path("players/<int:pk>/", views.PlayerUpdateView.as_view(), name="player-update"),
    path("players/<int:pk>/delete/", views.PlayerDeleteView.as_view(), name="player-delete"),
    path("owners/", views.OwnerListView.as_view(), name="owner-list"),
    path("owners/add/", views.OwnerCreateView.as_view(), name="owner-add"),
    path("owners/<int:pk>/", views.OwnerUpdateView.as_view(), name="owner-update"),
    path("owners/<int:pk>/delete/", views.OwnerDeleteView.as_view(), name="owner-delete"),
    path("teams/", views.TeamListView.as_view(), name="team-list"),
    path("teams/add/", views.TeamCreateView.as_view(), name="team-add"),
    # path("teams/<int:pk>/", views.TeamUpdateView.as_view(), name="team-update"),
    path("rosters/<int:teamId>/", views.TeamView, name="team-roster"),
    path("rosters/", views.TeamView, name="team-roster"),
    path("protection-lists/<int:teamId>", views.TeamProtectionList, name="team-protection-list"),
    path("protection-lists/", views.TeamProtectionList, name="team-protection-list"),
    path("teams/<int:pk>/delete/", views.TeamDeleteView.as_view(), name="team-delete"),
    path("rosters/", views.RosterListView.as_view(), name="roster-list"),
    path("rosters/add/", views.RosterCreateView, name="roster-add"),
    path("daflLogin/<str:username>/<slug:password>", views.DAFLLogin, name="dafl-login"),
    path("logout", views.logout_view, name="logout"),
    url('player-autocomplete/$', autocomplete.Select2QuerySetView.as_view(model=Player), name='player-autocomplete'),
    path("GetPositionsForPlayer/<int:playerId>/", views.GetPositionsForPlayer, name='GetPositionsForPlayer'),
    url("autocomplete", views.BasicDALView, name='autocomplete'),
]

urlpatterns += staticfiles_urlpatterns()