from django import forms
from .models import Product, ProductType, Transaction

class CreateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'productType', 'stock', 'status']
        widgets = {
            'productType': forms.Select(choices=ProductType.objects.all,),
            'status': forms.Select(choices=Product.STATUS_CHOICES,)
        }

class UpdateProductForm(forms.ModelForm):  
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'productType', 'stock', 'status']
        widgets = {
            'productType': forms.Select(choices=ProductType.objects.all,),
            'status': forms.Select(choices=Product.STATUS_CHOICES,)
        }