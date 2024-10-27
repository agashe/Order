from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("orders", views.orders, name="orders"),
    path("orders/<str:code>", views.order, name="order"),
]