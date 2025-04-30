from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Commission, Job, JobApplication
from.forms import JobApplicationForm
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
    template_name = 'commissions/commission_detail.html'

    def get_success_url(self):
        return reverse_lazy('commissions:commission-detail', kwargs={'pk': self.get_object().pk})
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        commission = ctx['commission']
        ctx['application_form'] = JobApplicationForm
        sumManpower=0
        acceptedManpower=0
        for job in Job.objects.filter(commission=commission):
            sumManpower+= job.manpowerRequired
            for applicant in JobApplication.objects.filter(job=job,status='B'):
                acceptedManpower+=1
        ctx['sumManpower'] = sumManpower
        ctx['openManpower'] = sumManpower-acceptedManpower
        return ctx
    
    def post(self, request, *args, **kwargs):
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            ja = form.save(commit=False)
            ja.applicant = self.request.user.profile
            ja.job = Job.objects.get(pk=request.POST.get('job'))
            ja.save()
            return redirect(self.get_success_url())
        else:
            print("FORM IS NOT")
            ctx = self.get_context_data(**kwargs)
            ctx['application_form'] = form
            return self.render_to_response(ctx)
