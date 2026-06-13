"""
Word Lists — Views
===================
"""

from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.core.permissions import IsCreatorOrReadOnly

from .models import Language, Quote, WordList
from .serializers import (
    LanguageSerializer,
    QuoteSerializer,
    WordListSerializer,
    WordListSummarySerializer,
)


class WordListListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/wordlists/     — List available word lists
    POST /api/v1/wordlists/     — Create a custom word list
    """

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["language__code", "difficulty", "is_public", "is_default"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "word_count", "times_used", "created_at"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return WordListSummarySerializer
        return WordListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = WordList.objects.select_related("language", "creator")
        if self.request.user.is_authenticated:
            # Show public lists + user's own private lists
            return queryset.filter(
                models.Q(is_public=True) | models.Q(creator=self.request.user)
            )
        return queryset.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class WordListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/wordlists/<id>/  — Get word list detail
    PATCH  /api/v1/wordlists/<id>/  — Update word list
    DELETE /api/v1/wordlists/<id>/  — Delete word list
    """

    serializer_class = WordListSerializer
    permission_classes = [IsCreatorOrReadOnly]
    queryset = WordList.objects.select_related("language", "creator")


class LanguageListView(generics.ListAPIView):
    """
    GET /api/v1/wordlists/languages/ — List available languages
    """

    serializer_class = LanguageSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Language.objects.filter(is_active=True)
    pagination_class = None  # No pagination for languages


class QuoteListView(generics.ListAPIView):
    """
    GET /api/v1/wordlists/quotes/ — List quotes for typing
    """

    serializer_class = QuoteSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["language__code", "difficulty"]
    queryset = Quote.objects.filter(is_active=True).select_related("language")

