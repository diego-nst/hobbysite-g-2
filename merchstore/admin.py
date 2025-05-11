from django.contrib import admin
from .models import Product, ProductType, Transaction


class ProductInLine(admin.TabularInline):
    model = Product


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    inlines = [ProductInLine]


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Transaction, TransactionAdmin)
