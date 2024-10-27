from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/<str:title>", views.show, name="show"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)