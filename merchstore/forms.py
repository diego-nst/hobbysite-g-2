from django import forms
from .models import Product, ProductType, Transaction

class CreateTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount' : forms.NumberInput(attrs={'min':'1'})
        }

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'productType', 'status']
        widgets = {
            'price': forms.NumberInput(attrs={'min':'1'}),
            'stock': forms.NumberInput(attrs={'min':'1'}),
            'productType': forms.Select(choices=ProductType.objects.all,),
            'status': forms.Select(choices=Product.STATUS_CHOICES,)
        }

class UpdateProductForm(forms.ModelForm):  
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'productType', 'status']
        widgets = {
            'productType': forms.Select(choices=ProductType.objects.all,),
            'status': forms.Select(choices=Product.STATUS_CHOICES,)
        }

class UpdateTransactionStatusForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Transaction.STATUS_CHOICES,),
        }