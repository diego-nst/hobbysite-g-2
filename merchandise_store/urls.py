from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(),name='product-list'),
    path('items', ProductListView.as_view(),name='product-list'),
    path('ítem/<int:pk>', ProductDetailView.as_view(),name='item'),
]

app_name = 'merchandise_store'