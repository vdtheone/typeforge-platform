"""
Core — Custom Middleware
=========================
"""

import logging
import time

logger = logging.getLogger(__name__)


class RequestTimingMiddleware:
    """
    Middleware that logs the time taken to process each request.
    Adds X-Request-Time header to responses.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        duration_ms = round(duration * 1000, 2)

        response["X-Request-Time"] = f"{duration_ms}ms"

        # Log slow requests (> 500ms)
        if duration > 0.5:
            logger.warning(
                "Slow request: %s %s took %sms",
                request.method,
                request.path,
                duration_ms,
            )

        return response
