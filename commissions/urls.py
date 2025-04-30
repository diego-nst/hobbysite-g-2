from django.urls import path
from .views import CommissionDetailView, CommissionListView,CommissionUpdateView

urlpatterns = [
    path('list', CommissionListView.as_view(), name='commission-list'),
    path('detail/<int:pk>', CommissionDetailView.as_view(), name='commission-detail'),
    path('<int:pk>/edit', CommissionUpdateView.as_view(), name='commission-edit')
]

app_name = 'commissions'
