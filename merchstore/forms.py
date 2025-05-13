from django import forms
from .models import Product, ProductType, Transaction


class CreateTransactionForm(forms.ModelForm):
    '''
    The class represents the form used when transactions are made.
    It asks the buyer for the amount of product they wish to transact.
    It is used in the ProductDetailView of the merchstore app's views.
    '''
    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '1'})
        }


class CreateProductForm(forms.ModelForm):
    '''
    The class represents the form filled out by the user when creating a new product.
    It asks the user for all fields except owner, which is automatically attributed to the user.
    It is used in the ProductCreateView of the merchstore app's views.
    '''
    class Meta:
        model = Product
        fields = ['name', 'description', 'price',
                  'stock', 'productType', 'status']
        widgets = {
            'price': forms.NumberInput(attrs={'min': '1'}),
            'stock': forms.NumberInput(attrs={'min': '1'}),
            'productType': forms.Select(choices=ProductType.objects.all,),
            'status': forms.Select(choices=Product.STATUS_CHOICES,)
        }


class UpdateProductForm(forms.ModelForm):
    '''
    The class represents the form filled out by the user to edit an existing product.
    It allows the user to edit all fields except owner.
    It is used in the ProductUpdateView of the merchstore app's views.
    '''
    class Meta:
        model = Product
        fields = ['name', 'description', 'price',
                  'stock', 'productType', 'status']
        widgets = {
            'productType': forms.Select(choices=ProductType.objects.all,),
            'status': forms.Select(choices=Product.STATUS_CHOICES,)
        }


class UpdateTransactionStatusForm(forms.ModelForm):
    '''
    The class represents the form filled out by a product's seller to edit an existing transaction.
    It allows the owner to edit a transaction's status.
    It is used in the TransactionDetailView of the merchstore app's views.
    '''
    class Meta:
        model = Transaction
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Transaction.STATUS_CHOICES,),
        }
