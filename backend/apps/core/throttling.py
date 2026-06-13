"""
Core — Custom Throttling Classes
==================================
"""

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    """Short burst rate limit (per minute)."""

    scope = "burst"


class SustainedRateThrottle(UserRateThrottle):
    """Sustained rate limit (per day)."""

    scope = "sustained"


class TestSubmitThrottle(UserRateThrottle):
    """Rate limit for typing test submissions."""

    scope = "test_submit"


class TestGenerateThrottle(UserRateThrottle):
    """Rate limit for test generation requests."""

    scope = "test_generate"


class AnonBurstThrottle(AnonRateThrottle):
    """Burst rate limit for anonymous users."""

    scope = "burst"
