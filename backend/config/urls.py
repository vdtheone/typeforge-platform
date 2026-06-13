"""
TypeForge Platform — Root URL Configuration
=============================================
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# =============================================================================
# API v1 URL Patterns
# =============================================================================
api_v1_patterns = [
    path("auth/", include("apps.accounts.urls.auth_urls")),
    path("users/", include("apps.accounts.urls.user_urls")),
    path("tests/", include("apps.typing_tests.urls")),
    path("results/", include("apps.results.urls")),
    path("wordlists/", include("apps.wordlists.urls")),
    path("themes/", include("apps.themes.urls")),
    path("analytics/", include("apps.analytics.urls")),
    path("leaderboards/", include("apps.leaderboards.urls")),
]

# =============================================================================
# Root URL Patterns
# =============================================================================
urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API v1
    path("api/v1/", include(api_v1_patterns)),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

# =============================================================================
# Debug & Development URLs
# =============================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns

# =============================================================================
# Admin Site Configuration
# =============================================================================
admin.site.site_header = "TypeForge Administration"
admin.site.site_title = "TypeForge Admin"
admin.site.index_title = "Dashboard"
