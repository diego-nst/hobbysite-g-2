from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class CommissionListView(ListView):
    template_name = 'commissions/commission_list.html'


class CommissionDetailView(DetailView):
    template_name = 'commissions/commission_detail.html'


def commission_list(request):
    ctx = {}
    return render(request, 'commissions/commission_list.html',ctx)


def commission_detail(request, pk):
    ctx = {}
    return render(request, 'commissions/commission_detail.html', ctx)
# Create your views here.
