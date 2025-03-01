from django.db import models
from django.urls import reverse

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merchandise_store:product-list', args=[str(self.name)])

    class Meta:
        ordering=['name'] #orders by name in ascending order

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    productType = models.ForeignKey(ProductType,
                                    on_delete=models.CASCADE,
                                    related_name="products",)

    def get_absolute_url(self):
        return reverse('merchandise_store:item', args=[str(self.pk)])

    class Meta:
        ordering=['name'] #orders by name in ascending order
