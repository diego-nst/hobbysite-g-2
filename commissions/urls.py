from django.urls import path
from .views import CommissionDetailView, CommissionListView, commission_list

urlpatterns = [
    path('commissions/list',commission_list,name='commission-list'),
    path('commissions/detail/<int:pk>',CommissionDetailView.as_view(),name='commission-detail')
]

app_name = 'commissions'
