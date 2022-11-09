"""Built-in python module"""
from typing import Any

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Women


class WomenAdmin(admin.ModelAdmin):
    """Class managing posts in admin-site"""

    list_display = ("id", "title", "time_create", "get_html_photo", "is_published")
    list_display_links = ("id", "title")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    list_filter = ("is_published", "time_create")
    prepopulated_fields = {"slug": ("title",)}
    fields = (
        "title",
        "slug",
        "cat",
        "content",
        "photo",
        "get_html_photo",
        "is_published",
        "time_create",
        "time_update",
    )
    readonly_fields = ("time_create", "time_update", "get_html_photo")
    save_on_top = True

    def get_html_photo(self, obj: Any) -> Any | None:
        """Getter photo"""
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=50>")
        return None

    get_html_photo.short_description = "Миниатюра"  # type: ignore


class CategoryAdmin(admin.ModelAdmin):
    """Class showing categories in admin-site"""

    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = "Админ-панель сайта о женщинах"
admin.site.site_header = "Админ-панель сайта о женщинах 2"
