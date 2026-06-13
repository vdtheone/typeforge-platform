"""
Themes — URLs
==============
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.ThemeListCreateView.as_view(), name="theme-list"),
    path("<int:pk>/", views.ThemeDetailView.as_view(), name="theme-detail"),
    path("<int:pk>/like/", views.ThemeLikeView.as_view(), name="theme-like"),
]
