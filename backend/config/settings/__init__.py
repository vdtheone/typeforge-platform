from .base import *  # noqa: F401,F403

# Default to development settings
try:
    from .development import *  # noqa: F401,F403
except ImportError:
    pass
