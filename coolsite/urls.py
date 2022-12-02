"""Url patterns"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from coolsite import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include("women.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

urlpatterns += [
    path("captcha/", include("captcha.urls")),
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]  # type:ignore
