from django.db import models
from django.urls import reverse
from accounts.models import Profile

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merchstore:product-list', args=[str(self.name)])

    def get_products(self):
        return self.products.all()

    class Meta:
        ordering = ['name']  # orders by name in ascending order
        verbose_name = "Product Type"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    productType = models.ForeignKey(ProductType,
                                    on_delete=models.SET_NULL,
                                    related_name="products",
                                    null=True)
    stock = models.IntegerField(default=-99)

    STATUS_CHOICES = {
        "AVAILABLE": "Available",
        "ON_SALE": "On sale",
        "NO_STOCK": "Out of stock",
    }
    status = models.CharField(max_length=255, 
                              choices=STATUS_CHOICES, 
                              default="AVAILABLE")
    # see documentation for reference re: choices parameter
    # https://docs.djangoproject.com/en/5.2/ref/models/fields/

    def get_absolute_url(self):
        return reverse('merchstore:item', args=[str(self.pk)])

    class Meta:
        ordering = ['name']  # orders by name in ascending order
        verbose_name = "Product"

class Transaction(models.Model):
    buyer = models.ForeignKey(Profile,
                              null=True,
                              on_delete=models.SET_NULL)
    product = models.ForeignKey(Product,
                                null=True,
                                on_delete=models.SET_NULL)
    amount = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    
    STATUS_CHOICES = {
        "ON_CART": "On cart",
        "TO_PAY": "To pay",
        "TO_SHIP": "To ship",
        "TO_RECEIVE": "To receive",
        "DELIVERED": "Delivered"
    }
    status = models.CharField(max_length=255,
                              choices=STATUS_CHOICES,
                              null=True)
    # see documentation for reference re: choices parameter
    # https://docs.djangoproject.com/en/5.2/ref/models/fields/

    # TO DO:
    # make Transaction (and its choices) functional
    # ensure that Product stock and status updates according to transactions
