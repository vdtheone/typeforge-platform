"""
Core — Custom Exception Handler
=================================
"""

import logging

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent JSON error responses.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "success": False,
            "error": {
                "code": response.status_code,
                "message": _get_error_message(exc, response),
                "details": _get_error_details(response.data),
            },
        }
        response.data = custom_data

    elif isinstance(exc, Exception):
        # Unhandled exception — log and return 500
        logger.exception("Unhandled exception: %s", exc)
        response = Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": "An unexpected error occurred.",
                    "details": None,
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response


def _get_error_message(exc, response):
    """Extract a human-readable error message."""
    if isinstance(exc, Http404):
        return "Resource not found."
    if isinstance(exc, ValidationError):
        return "Validation error."
    if hasattr(exc, "detail"):
        if isinstance(exc.detail, str):
            return exc.detail
        if isinstance(exc.detail, list) and len(exc.detail) > 0:
            return str(exc.detail[0])
    # Fallback to status text
    return response.status_text if hasattr(response, "status_text") else "Error"


def _get_error_details(data):
    """Format error details consistently."""
    if isinstance(data, dict):
        # Check if it's already our custom format
        if "success" in data:
            return data.get("error", {}).get("details")
        # DRF validation errors
        return {key: val if isinstance(val, list) else [val] for key, val in data.items()}
    if isinstance(data, list):
        return data
    return None


class TypeForgeAPIException(APIException):
    """Base exception for TypeForge-specific errors."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A platform error occurred."
    default_code = "platform_error"


class AntiCheatViolation(TypeForgeAPIException):
    """Raised when anti-cheat checks detect suspicious activity."""

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Suspicious activity detected. Result has been flagged."
    default_code = "anti_cheat_violation"


class TestGenerationError(TypeForgeAPIException):
    """Raised when test generation fails."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Failed to generate typing test."
    default_code = "test_generation_error"
