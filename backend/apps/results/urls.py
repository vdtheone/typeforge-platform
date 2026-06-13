"""
Results — URLs
===============
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.ResultListView.as_view(), name="result-list"),
    path("stats/", views.ResultStatsView.as_view(), name="result-stats"),
    path("personal-bests/", views.PersonalBestsView.as_view(), name="personal-bests"),
    path("<int:pk>/", views.ResultDetailView.as_view(), name="result-detail"),
]
