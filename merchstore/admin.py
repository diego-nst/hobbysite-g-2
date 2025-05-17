from django.contrib import admin
from .models import Product, ProductType, Transaction


class ProductInLine(admin.TabularInline):
    '''
    InLine for the Product model under the ProductType model.
    '''
    model = Product


class ProductTypeAdmin(admin.ModelAdmin):
    '''
    Admin for the ProductType model. 
    It has one inline, which is the Product model.
    '''
    model = ProductType
    inlines = [ProductInLine]


class TransactionAdmin(admin.ModelAdmin):
    '''
    Admin for the Transaction model.
    '''
    model = Transaction


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Transaction, TransactionAdmin)
