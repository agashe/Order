from django.db import models
from inventory.models import Product
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    code = models.CharField(max_length=200)
    notes = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    def url(self):
        return '/orders/' + self.code

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)