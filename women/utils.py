"""Django func to cache and django class aggregator"""
from django.core.cache import cache
from django.db.models import Count

from .models import Category

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
]


class DataMixin:  # pylint: disable=too-few-public-methods
    """Class for pagination"""

    paginate_by = 20

    def get_user_context(self, **kwargs) -> dict:
        """Func getter info about user"""
        context = kwargs
        cats = cache.get("cats")
        if not cats:
            cats = Category.objects.annotate(Count("women"))
            cache.set("cats", cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:  # type: ignore
            user_menu.pop(1)

        context["menu"] = user_menu
        context["cats"] = cats
        if "cat_selected" not in context:
            context["cat_selected"] = 0
        return context
