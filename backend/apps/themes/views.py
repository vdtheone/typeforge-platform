"""
Themes — Views
===============
"""

from django.db import models
from django.db.models import F
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.permissions import IsCreatorOrReadOnly

from .models import Theme, ThemeLike
from .serializers import ThemeSerializer, ThemeSummarySerializer


class ThemeListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/themes/     — List themes
    POST /api/v1/themes/     — Create a theme
    """

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ThemeSummarySerializer
        return ThemeSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = Theme.objects.select_related("creator")
        if self.request.user.is_authenticated:
            return queryset.filter(
                models.Q(is_public=True) | models.Q(creator=self.request.user)
            )
        return queryset.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ThemeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/themes/<id>/  — Theme detail
    PATCH  /api/v1/themes/<id>/  — Update theme
    DELETE /api/v1/themes/<id>/  — Delete theme
    """

    serializer_class = ThemeSerializer
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Theme.objects.select_related("creator")


class ThemeLikeView(APIView):
    """
    POST /api/v1/themes/<id>/like/ — Toggle like on a theme
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            theme = Theme.objects.get(pk=pk)
        except Theme.DoesNotExist:
            return Response(
                {"success": False, "error": "Theme not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        like, created = ThemeLike.objects.get_or_create(
            user=request.user,
            theme=theme,
        )

        if created:
            # Liked
            Theme.objects.filter(pk=pk).update(likes_count=F("likes_count") + 1)
            return Response(
                {"success": True, "liked": True, "likes_count": theme.likes_count + 1}
            )
        else:
            # Unlike
            like.delete()
            Theme.objects.filter(pk=pk).update(likes_count=F("likes_count") - 1)
            return Response(
                {"success": True, "liked": False, "likes_count": max(0, theme.likes_count - 1)}
            )
