"""
Accounts — Views
=================
"""

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    PublicProfileSerializer,
    UserDetailSerializer,
    UserPreferencesSerializer,
)

User = get_user_model()


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/v1/users/me/ — Get current user profile
    PATCH /api/v1/users/me/ — Update current user profile
    """

    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserPreferencesView(APIView):
    """
    GET   /api/v1/users/me/preferences/ — Get user preferences
    PATCH /api/v1/users/me/preferences/ — Update user preferences
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        preferences = {**profile.default_preferences, **profile.preferences}
        return Response({"success": True, "data": preferences})

    def patch(self, request):
        serializer = UserPreferencesSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        profile = request.user.profile
        profile.preferences.update(serializer.validated_data)
        profile.save(update_fields=["preferences", "updated_at"])

        preferences = {**profile.default_preferences, **profile.preferences}
        return Response({"success": True, "data": preferences})


class PublicProfileView(generics.RetrieveAPIView):
    """
    GET /api/v1/users/<username>/ — Get public profile
    """

    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "username"
    queryset = User.objects.filter(is_active=True).select_related("profile")
