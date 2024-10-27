from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def url(self):
        return '/products/category/' + str(self.id) + '/' + self.name.replace(" ", "-")

    class Meta:
        verbose_name_plural = "categories"

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def thumbnail(self):
        try:
            return self.productimage_set.first().image.url
        except:
            return ''

    def url(self):
        return '/products/show/' + str(self.id) + '/' + self.title.replace(" ", "-")

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    image = models.FileField()
