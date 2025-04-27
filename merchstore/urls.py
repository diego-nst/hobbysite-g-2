from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView #, CartView, TransactionListView

urlpatterns = [
    path('merchstore/items', ProductListView.as_view(), name='product-list'),
    path('merchstore/item/<int:pk>', ProductDetailView.as_view(), name='item'),
    path('merchstore/item/add', ProductCreateView.as_view(), name='create-product'),
    path('merchstore/item/<int:pk>/edit', ProductUpdateView.as_view(), name='update-product'),
    # path('merchstore/cart', CartView.as_view(), name='cart'),
    # path('merchstore/transactions', TransactionListView.as_view(), name='transaction-list'),
]

app_name = 'merchstore'
