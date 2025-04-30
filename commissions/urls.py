from django.urls import path
from .views import CommissionDetailView, CommissionListView,CommissionUpdateView,CommissionCreateView

urlpatterns = [
    path('list', CommissionListView.as_view(), name='commission-list'),
    path('detail/<int:pk>', CommissionDetailView.as_view(), name='commission-detail'),
    path('<int:pk>/edit', CommissionUpdateView.as_view(), name='commission-edit'),
    path('add', CommissionCreateView.as_view(), name='commission-add')
]

app_name = 'commissions'
