from django.urls import path
from .views import (ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, 
                    CartView, TransactionListView, TransactionDetailView)

urlpatterns = [
    path('items', ProductListView.as_view(), name='product-list'),
    path('item/<int:pk>', ProductDetailView.as_view(), name='item'),
    path('item/add', ProductCreateView.as_view(), name='create-product'),
    path('item/<int:pk>/edit', ProductUpdateView.as_view(), name='update-product'),
    path('cart', CartView.as_view(), name='cart'),
    path('transactions', TransactionListView.as_view(), name='transactions-list'),
    path('transactions/<int:pk>', TransactionDetailView.as_view(), name='transaction'),
]

app_name = 'merchstore'
