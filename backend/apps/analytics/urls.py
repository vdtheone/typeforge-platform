"""
Analytics — URLs
=================
"""

from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.AnalyticsDashboardView.as_view(), name="analytics-dashboard"),
    path("wpm-trend/", views.WPMTrendView.as_view(), name="wpm-trend"),
    path("accuracy-trend/", views.AccuracyTrendView.as_view(), name="accuracy-trend"),
    path("weak-keys/", views.WeakKeysView.as_view(), name="weak-keys"),
]
