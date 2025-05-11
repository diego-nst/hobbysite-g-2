from django.db import models
from django.urls import reverse
from user_management.models import Profile

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
        verbose_name = 'Product Type'


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, 
                                decimal_places=2, 
                                default=1)
    productType = models.ForeignKey(ProductType,
                                    on_delete=models.SET_NULL,
                                    related_name='products',
                                    null=True)
    stock = models.IntegerField(default=1)
    owner = models.ForeignKey(Profile,
                              on_delete=models.CASCADE,
                              related_name='products',
                              null=True,
                              )

    STATUS_CHOICES = {
        'AVAILABLE': 'Available',
        'ON_SALE': 'On sale',
        'NO_STOCK': 'Out of stock',
    }
    status = models.CharField(max_length=255, 
                              choices=STATUS_CHOICES, 
                              default='AVAILABLE')
    # see documentation for reference re: choices parameter
    # https://docs.djangoproject.com/en/5.2/ref/models/fields/

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('merchstore:item', args=[str(self.pk)])
    
    def save(self, *args, **kwargs):
        if self.stock <= 0:
            self.STATUS_CHOICES = 'NO_STOCK'
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']  # orders by name in ascending order
        verbose_name = 'Product'

class Transaction(models.Model):
    buyer = models.ForeignKey(Profile,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='transactions')
    product = models.ForeignKey(Product,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name='transactions')
    amount = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    
    STATUS_CHOICES = {
        'IN_CART': 'On cart',
        'TO_PAY': 'To pay',
        'TO_SHIP': 'To ship',
        'TO_RECEIVE': 'To receive',
        'DELIVERED': 'Delivered'
    }

    status = models.CharField(max_length=255,
                              choices=STATUS_CHOICES,
                              null=True)
    
    def get_absolute_url(self):
        return reverse('merchstore:transaction', args=[str(self.pk)])
    
    class Meta:
        ordering = ['buyer', 'created_on']
        verbose_name = 'Transaction'

    # see documentation for reference re: choices parameter
    # https://docs.djangoproject.com/en/5.2/ref/models/fields/
