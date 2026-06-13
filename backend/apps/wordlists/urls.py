"""
Word Lists — URLs
==================
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.WordListListCreateView.as_view(), name="wordlist-list"),
    path("<int:pk>/", views.WordListDetailView.as_view(), name="wordlist-detail"),
    path("languages/", views.LanguageListView.as_view(), name="language-list"),
    path("quotes/", views.QuoteListView.as_view(), name="quote-list"),
]
