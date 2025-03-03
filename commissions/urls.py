from django.urls import path
from .views import CommissionDetailView, CommissionListView, commission_list, commission_detail

urlpatterns = [
    path('commissions/list',commission_list,name='commission-list'),
    path('commissions/detail/<int:pk>',commission_detail,name='commission-detail')
]

app_name = 'commissions'
