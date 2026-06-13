"""
Core — Custom Permissions
==========================
"""

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Object-level permission: only the owner can access the object.
    Expects the object to have a `user` field.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission: owner can edit, others can read.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.user == request.user


class IsCreatorOrReadOnly(BasePermission):
    """
    Object-level permission for models with a `creator` field.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.creator == request.user
