"""
Accounts — User URLs
=====================
"""

from django.urls import path

from apps.accounts.views import CurrentUserView, PublicProfileView, UserPreferencesView

urlpatterns = [
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("me/preferences/", UserPreferencesView.as_view(), name="user-preferences"),
    path("<str:username>/", PublicProfileView.as_view(), name="public-profile"),
]
