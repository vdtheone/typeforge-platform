"""
Core — Utility Functions
==========================
"""

import hashlib
import random
import string
import time
from functools import wraps

from django.core.cache import cache


def generate_slug(length=8):
    """Generate a random alphanumeric slug."""
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))


def cache_result(key_prefix, timeout=300):
    """
    Decorator to cache function results in Redis.

    Usage:
        @cache_result("user_stats", timeout=600)
        def get_user_stats(user_id):
            ...
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build cache key from function args
            key_parts = [key_prefix] + [str(a) for a in args]
            key_parts += [f"{k}={v}" for k, v in sorted(kwargs.items())]
            cache_key = ":".join(key_parts)
            cache_key = hashlib.md5(cache_key.encode()).hexdigest()
            cache_key = f"{key_prefix}:{cache_key}"

            result = cache.get(cache_key)
            if result is not None:
                return result

            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result

        wrapper.invalidate = lambda *args, **kwargs: cache.delete(
            f"{key_prefix}:{hashlib.md5(':'.join([key_prefix] + [str(a) for a in args] + [f'{k}={v}' for k, v in sorted(kwargs.items())]).encode()).hexdigest()}"
        )
        return wrapper

    return decorator


def calculate_net_wpm(characters_typed, errors, duration_seconds):
    """
    Calculate Net WPM.
    Net WPM = (Characters Typed / 5 - Errors) / Minutes
    """
    if duration_seconds <= 0:
        return 0.0
    minutes = duration_seconds / 60
    gross_wpm = (characters_typed / 5) / minutes
    net_wpm = max(0, gross_wpm - (errors / minutes))
    return round(net_wpm, 2)


def calculate_raw_wpm(characters_typed, duration_seconds):
    """
    Calculate Raw WPM (no error penalty).
    Raw WPM = (Characters Typed / 5) / Minutes
    """
    if duration_seconds <= 0:
        return 0.0
    minutes = duration_seconds / 60
    return round((characters_typed / 5) / minutes, 2)


def calculate_accuracy(correct_chars, total_chars):
    """Calculate typing accuracy as a percentage."""
    if total_chars <= 0:
        return 0.0
    return round((correct_chars / total_chars) * 100, 2)


def calculate_consistency(wpm_samples):
    """
    Calculate typing consistency based on WPM variance.
    Returns a score from 0-100 where 100 is perfectly consistent.
    """
    if not wpm_samples or len(wpm_samples) < 2:
        return 100.0

    mean = sum(wpm_samples) / len(wpm_samples)
    if mean == 0:
        return 0.0

    variance = sum((x - mean) ** 2 for x in wpm_samples) / len(wpm_samples)
    std_dev = variance**0.5
    coefficient_of_variation = std_dev / mean

    # Convert to 0-100 scale (lower CV = higher consistency)
    consistency = max(0, 100 * (1 - coefficient_of_variation))
    return round(consistency, 2)


def timing():
    """Simple context manager for timing code blocks."""

    class Timer:
        def __enter__(self):
            self.start = time.time()
            return self

        def __exit__(self, *args):
            self.end = time.time()
            self.duration = self.end - self.start
            self.duration_ms = round(self.duration * 1000, 2)

    return Timer()
