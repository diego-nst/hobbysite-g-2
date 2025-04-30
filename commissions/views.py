from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job, JobApplication
from.forms import JobApplicationForm, CommissionForm, JobForm
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
        
class CommissionUpdateView(LoginRequiredMixin,DetailView):
    model = Commission
    template_name= 'commissions/commission_edit.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = CommissionForm(instance=self.get_object())
        ctx['job_form'] = JobForm()
        ctx['apply_form'] = JobApplicationForm
        
        sumManpower=0
        acceptedManpower=0
        for job in Job.objects.filter(commission=self.get_object()):
            sumManpower+= job.manpowerRequired
            for applicant in JobApplication.objects.filter(job=job,status='B'):
                acceptedManpower+=1
        ctx['sumManpower'] = sumManpower
        ctx['openManpower'] = sumManpower-acceptedManpower


    
        return ctx
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        if('commission-edit' in request.POST):
            form = CommissionForm(request.POST)
            if form.is_valid():
                c = self.get_object()
                c.title = request.POST.get('title')
                c.description = request.POST.get('description')
                c.status = request.POST.get('status')
                c.save()
                return redirect(self.get_success_url())
            else:
                print("FORM IS NOT")
                ctx = self.get_context_data(**kwargs)
                ctx['form'] = form
                return self.render_to_response(ctx)
        elif('job-create' in request.POST):
            jform = JobForm(request.POST)
            if jform.is_valid():
                j = Job()
                j.commission = self.get_object()
                j.role = request.POST.get('role')
                j.manpowerRequired = request.POST.get('manpowerRequired')    
                j.save()
                return redirect(reverse_lazy('commissions:commission-edit', kwargs={'pk': self.get_object().pk}))
            else:
                print("FORM IS NOT")
                ctx = self.get_context_data(**kwargs)
                ctx['form'] = form
                return self.render_to_response(ctx)
        else:
            jaform = JobApplicationForm(request.POST)
            if jaform.is_valid():
                ja = JobApplication.objects.get(pk=request.POST.get('jobApplication'))
                j = ja.job
                ja.status = 'B' if('job-accept' in request.POST) else 'C'
                accepted=0
                ja.save()
                for applicant in JobApplication.objects.filter(job=j,status='B'):
                    accepted+=1
                if(accepted >= j.manpowerRequired):
                    j.status='B'
                j.save()

                return redirect(reverse_lazy('commissions:commission-edit', kwargs={'pk': self.get_object().pk}))
            else:
                print("FORM IS NOT")
                ctx = self.get_context_data(**kwargs)
                ctx['form'] = form
                return self.render_to_response(ctx)
                    
        

    def get_success_url(self):
        return reverse_lazy('commissions:commission-detail', kwargs={'pk': self.get_object().pk})
