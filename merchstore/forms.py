from django import forms
from .models import Product, ProductType, Transaction
from django.core.validators import MinValueValidator

class CreateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # amount = forms.fields.IntegerField(min_value=1)
        fields = ['amount']
        widgets = {
            'amount' : forms.NumberInput(attrs={'min':'1'})
        }

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'productType', 'stock', 'status']
        widgets = {
            'price': forms.NumberInput(attrs={'min':'1'}),
            'stock': forms.NumberInput(attrs={'min':'1'}),
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