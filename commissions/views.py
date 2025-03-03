from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Commission


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/commission_detail.html'


def commission_list(request):
    ctx = {"commissions": Commission.objects.all()}
    return render(request, 'commissions/commission_list.html',ctx)


def commission_detail(request, pk):
    commission = Commission.objects.get(pk=pk)
    comments = commission.comments.all()
    ctx = {"commission": commission,
           "comments": comments}
    return render(request, 'commissions/commission_detail.html', ctx)
