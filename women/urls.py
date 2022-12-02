# noqa: I001, I005
"""Django-func path"""
from django.urls import path

# from . import admin
from .views import (AddPage, ContactFormView, LoginUser, RegisterUser,
                    ShowPost, WomenAdmin, WomenCategory, WomenHome, about,
                    logout_user)

urlpatterns = [
    path("", WomenHome.as_view(), name="home"),
    path("about/", about, name="about"),
    path("addpage/", AddPage.as_view(), name="add_page"),
    path("contact/", ContactFormView.as_view(), name="contact"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("post/<slug:post_slug>/", ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", WomenCategory.as_view(), name="category"),
]
