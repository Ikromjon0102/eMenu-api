from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=150)

    def __str__(self):
        return self.category_name
    
# class Product(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     base_price = models.DecimalField(max_digits=10, decimal_places=2)
#     product_image = models.ImageField(upload_to='products/', blank=True, null=True)
#
#     objects = models.Manager
#
#     def __str__(self):
#         return self.name
#
#
# class ProductVariation(models.Model):
#     product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
#     size = models.CharField(max_length=50, blank=True, null=True)
#     color = models.CharField(max_length=50, blank=True, null=True)
#     additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     stock = models.IntegerField(default=0)
#
#     class Meta:
#         unique_together = ('product', 'size', 'color')
#
#     def __str__(self):
#         return f'{self.product.name} - Size: {self.size} - Color: {self.color}'
#
#     @property
#     def total_price(self):
#         return self.product.base_price + self.additional_price




from django.db import models

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    product_image = models.ImageField(upload_to='products/', null=True, blank=True)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
