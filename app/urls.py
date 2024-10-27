from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home.urls")),
    path('products/', include("inventory.urls")),
    path('shop/', include("shop.urls")),
    path('blog/', include("blog.urls")),
    path('user/', include("user.urls")),
]
