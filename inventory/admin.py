from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price')

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
