"""Women tags"""
from typing import Any

from django import template
from django.db.models import QuerySet

from women.models import Category

register = template.Library()


@register.simple_tag(name="getcats")
def get_categories(_filter=None) -> QuerySet[Any]:
    """getter list of categories"""
    if not _filter:
        return Category.objects.all()
    return Category.objects.filter(pk=_filter)


@register.inclusion_tag("women/list_categories.html")
def show_categories(_sort=None, cat_selected=0) -> dict:
    """Show categories"""
    if not _sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(_sort)

    return {"cats": cats, "cat_selected": cat_selected}
