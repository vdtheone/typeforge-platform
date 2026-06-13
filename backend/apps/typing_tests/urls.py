"""
Typing Tests — URLs
====================
"""

from django.urls import path

from . import views

urlpatterns = [
    path("generate/", views.TestGenerateView.as_view(), name="test-generate"),
    path("submit/", views.TestSubmitView.as_view(), name="test-submit"),
]
