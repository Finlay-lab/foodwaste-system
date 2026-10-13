from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.core.views import health, home

api_router = DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    path("api/", include(api_router.urls)),
    path("accounts/", include("apps.accounts.urls")),
    path("business/", include("apps.business.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("", home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
