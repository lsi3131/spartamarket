from django.urls import path
from django import forms
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("delete/", views.delete, name="delete"),
    path("update/", views.update, name="update"),
    path("password/", views.change_password, name="change_password"),
    path("profile/", views.profile, name="profile"),
    path("check_name_dup/", views.check_name_dup, name="check_name_dup"),
    path("user_list/", views.user_list, name="user_list"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    # path("", views.login, name="login"),
]

