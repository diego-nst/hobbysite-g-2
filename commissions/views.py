from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Commission, Job, JobApplication
from django.urls import reverse_lazy
from django.shortcuts import redirect

class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        if(self.request.user.is_authenticated):
            applied = set()
            for application in JobApplication.objects.filter(applicant=self.request.user.profile):
                applied.add(application.job.commission)
            ctx['created_commissions']= Commission.objects.filter(author=self.request.user.profile)
            ctx['applied_commissions']=applied
        ctx['commissions']=Commission.objects.all()
        return ctx


class CommissionDetailView(DetailView):
    model = Commission
    context_object_name = 'commission'
    template_name = 'commissions/commission_detail.html'
