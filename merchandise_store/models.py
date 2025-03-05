from django.db import models
from django.urls import reverse

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merchandise_store:product-list', args=[str(self.name)])

    def get_products(self):
        return self.products.all()
    
    class Meta:
        ordering=['name'] #orders by name in ascending order
        verbose_name="Product Type"

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    productType = models.ForeignKey(ProductType,
                                    on_delete=models.SET_NULL,
                                    related_name="products",
                                    null=True)

    def get_absolute_url(self):
        return reverse('merchandise_store:item', args=[str(self.pk)])

    class Meta:
        ordering=['name'] #orders by name in ascending order
        verbose_name="Product"
