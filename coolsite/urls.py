"""Url patterns"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from coolsite import settings
from women.views import page_not_found

urlpatterns = [
    path("admin/", admin.site.urls),
    path("captcha/", include("captcha.urls")),
    path("", include("women.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )  # type:ignore

handler404 = page_not_found
