from django.urls import path
from .views import CommissionDetailView, CommissionListView

urlpatterns = [
    path('commissions/list', CommissionListView.as_view(), name='commission-list'),
    path('commissions/detail/<int:pk>', CommissionDetailView.as_view(), name='commission-detail')
]

app_name = 'commissions'
