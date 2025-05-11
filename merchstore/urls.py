from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView
from .views import CartView, TransactionListView, TransactionDetailView

urlpatterns = [
    path('merchstore/items', ProductListView.as_view(), name='product-list'),
    path('merchstore/item/<int:pk>', ProductDetailView.as_view(), name='item'),
    path('merchstore/item/add', ProductCreateView.as_view(), name='create-product'),
    path('merchstore/item/<int:pk>/edit', ProductUpdateView.as_view(), name='update-product'),
    path('merchstore/cart', CartView.as_view(), name='cart'),
    path('merchstore/transactions', TransactionListView.as_view(), name='transactions-list'),
    path('merchstore/transactions/<int:pk>', TransactionDetailView.as_view(), name='transaction'),
]

app_name = 'merchstore'
