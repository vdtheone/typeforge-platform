"""
TypeForge Platform — Development Settings
==========================================
"""

from .base import *  # noqa: F401,F403

# =============================================================================
# DEBUG
# =============================================================================
DEBUG = True

# =============================================================================
# ALLOWED HOSTS
# =============================================================================
ALLOWED_HOSTS = ["*"]

# =============================================================================
# INSTALLED APPS — Dev Extras
# =============================================================================
INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
    "django_extensions",
]

# =============================================================================
# MIDDLEWARE — Debug Toolbar
# =============================================================================
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

# =============================================================================
# DEBUG TOOLBAR
# =============================================================================
INTERNAL_IPS = ["127.0.0.1", "localhost"]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
}

# =============================================================================
# EMAIL — Console Backend
# =============================================================================
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# =============================================================================
# REST FRAMEWORK — Allow Browsable API in Dev
# =============================================================================
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

# =============================================================================
# CORS — Allow All in Dev
# =============================================================================
CORS_ALLOW_ALL_ORIGINS = True

# =============================================================================
# DATABASE — SQLite fallback for local development without PostgreSQL
# Comment this block out when using PostgreSQL via Docker
# =============================================================================
import os

from decouple import config as decouple_config

if decouple_config("USE_SQLITE", default="false", cast=bool):
    DATABASES = {  # noqa: F405
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        }
    }

# =============================================================================
# LOGGING — Debug Level
# =============================================================================
LOGGING["loggers"]["django.db.backends"] = {  # noqa: F405
    "handlers": ["console"],
    "level": "WARNING",
    "propagate": False,
}
