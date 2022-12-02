"""Django classes and funcs for creating views"""
from typing import Any

from django.contrib import admin
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, FormView, ListView

from . import forms, models
from .models import Category, Women
from .utils import DataMixin, menu


class WomenHome(DataMixin, ListView):  # # pylint: disable=too-many-ancestors
    """Home page logic"""

    model = models.Women
    template_name = "women/index.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self) -> QuerySet[Any]:
        return models.Women.objects.filter(is_published=True).select_related("cat")


def about(request: HttpRequest) -> HttpResponse:
    """Page 404"""
    return render(request, "women/about.html", {"menu": menu, "title": "О сайте"})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    """Page getter"""

    form_class = forms.AddPostForm
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("home")
    raise_exception = True

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    """Creator of contact form"""

    form_class = forms.ContactForm
    template_name = "women/contact.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self) -> HttpResponse:   # type: ignore
        return redirect("home")


def page_not_found() -> HttpResponse:
    """Page 404"""
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class ShowPost(DataMixin, DetailView):
    """Post getter"""

    model = models.Women
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["post"])
        return dict(list(context.items()) + list(c_def.items()))


class WomenCategory(DataMixin, ListView):
    """Category getter"""

    model = models.Women
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return models.Women.objects.filter(
            cat__slug=self.kwargs["cat_slug"], is_published=True
        ).select_related("cat")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        objs = models.Category.objects.get(slug=self.kwargs["cat_slug"])
        objs_def = self.get_user_context(
            title="Категория - " + str(objs.name), cat_selected=objs.pk
        )
        return dict(list(context.items()) + list(objs_def.items()))


class RegisterUser(DataMixin, CreateView):
    """Creator registration form"""

    form_class = forms.RegisterUserForm
    template_name = "women/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form) -> HttpResponse:
        user = form.save()
        login(self.request, user)
        return redirect("home")


class LoginUser(DataMixin, LoginView):
    """Loginer"""

    form_class = forms.LoginUserForm
    template_name = "women/login.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self) -> str:
        return reverse_lazy("home")


def logout_user(request: HttpRequest) -> HttpResponse:
    """Logouter"""
    logout(request)
    return redirect("login")


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

    def get_html_photo(self, obj: Any) -> Any | None:  # type: ignore
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
