from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("terms-of-usage", views.terms_of_usage, name="terms_of_usage"),
    path("privacy-policy", views.privacy_policy, name="privacy_policy"),
    path("delivery-information", views.delivery_information, name="delivery_information"),
    path("subscribe", views.subscribe, name="subscribe"),
]