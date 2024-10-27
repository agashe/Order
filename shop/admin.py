from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'total', 'created_at', 'updated_at')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'quantity', 'total')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'country', 'state', 'city')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Address, AddressAdmin)
