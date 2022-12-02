"""Django-func path"""
from django.urls import path

from . import admin
from .views import (AddPage, ContactFormView, LoginUser, RegisterUser,
                    ShowPost, WomenCategory, WomenHome, about, logout_user, WomenAdmin)

urlpatterns = [
    path("", WomenHome.as_view(), name="home"),
    path("admin/", WomenAdmin.as_view(), name="admin"),
    path("about/", about, name="about"),
    path("addpage/", AddPage.as_view(), name="add_page"),
    path("contact/", ContactFormView.as_view(), name="contact"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("post/<slug:post_slug>/", ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", WomenCategory.as_view(), name="category"),
]
