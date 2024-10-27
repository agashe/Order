from django.urls import path
from . import views

urlpatterns = [
    path("login", views.log_in, name="log_in"),
    path("register", views.register, name="register"),
    path("logout", views.log_out, name="log_out"),
    path("profile", views.profile, name="profile"),
]