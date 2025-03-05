from django.contrib import admin
from .models import Product, ProductType

class ProductInLine(admin.TabularInline):
    model = Product

class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    inlines = [ProductInLine]

admin.site.register(ProductType, ProductTypeAdmin)
