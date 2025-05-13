from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobForm


class CommissionListView(ListView):
    ''' 
    List view for the Commission model
    
    Displays all the objects under the commission app 
    Displays commissions created and applied to if user is logged in
    '''
    model = Commission
    template_name = 'commissions/commission_list.html'

    def get_context_data(self, **kwargs):
        '''
        adds information to context if user is logged in
        displays commissions created and applied to
        '''
        ctx = super().get_context_data(**kwargs)

        if (self.request.user.is_authenticated):
            applied = set()
            for application in JobApplication.objects.filter(applicant=self.request.user.profile):
                applied.add(application.job.commission)
            ctx['created_commissions'] = Commission.objects.filter(
                author=self.request.user.profile)
            ctx['applied_commissions'] = applied
        ctx['commissions'] = Commission.objects.all()
        return ctx


class CommissionDetailView(DetailView):
    '''
    Detail view for the Commission model

    Displays all information in the Commission model, the Jobs connected to the Commission, and the Job Applications connected to the Job
    Allows logged in users to apply for open Jobs and allows the author to access the update view
    '''
    model = Commission
    template_name = 'commissions/commission_detail.html'

    def get_success_url(self):
        return reverse_lazy('commissions:commission-detail', kwargs={'pk': self.get_object().pk})

    def get_context_data(self, **kwargs):
        '''adds information to context: calculates sum manpower and open manpower'''
        ctx = super().get_context_data(**kwargs)
        commission = ctx['commission']
        sumManpower = 0
        acceptedManpower = 0
        for job in Job.objects.filter(commission=commission):
            sumManpower += job.manpowerRequired
            for applicant in JobApplication.objects.filter(job=job, status='B'):
                acceptedManpower += 1
        ctx['sumManpower'] = sumManpower
        ctx['openManpower'] = sumManpower-acceptedManpower
        return ctx

    def post(self, request, *args, **kwargs):
        '''adds a post to make an application based on the button of the job pressed'''
        ja = JobApplication()
        ja.applicant = self.request.user.profile
        ja.job = Job.objects.get(pk=request.POST.get('job'))
        ja.save()
        return redirect(self.get_success_url())


class CommissionUpdateView(LoginRequiredMixin, DetailView):
    '''
    Update View accessible if the user is the author

    Allows author to edit details and status of commission
    Allows author to create new jobs and
    Allows author to accept/reject job applicaations    
    '''
    model = Commission
    template_name = 'commissions/commission_edit.html'

    def get_context_data(self, **kwargs):
        '''
        adds information to context: calculates sum manpower and open manpower
        also adds the different forms
        '''
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = CommissionForm(instance=self.get_object())
        ctx['job_form'] = JobForm()

        sumManpower = 0
        acceptedManpower = 0
        for job in Job.objects.filter(commission=self.get_object()):
            sumManpower += job.manpowerRequired
            for applicant in JobApplication.objects.filter(job=job, status='B'):
                acceptedManpower += 1
        ctx['sumManpower'] = sumManpower
        ctx['openManpower'] = sumManpower-acceptedManpower

        return ctx

    def post(self, request, *args, **kwargs):
        '''
        uses if statements for the different amount of posts
        commission-edit - main update form that changes the commission itself
        job-create - form to add jobs to the commission
        job-accept/job-reject - form to accept/reject applications under a job
        '''
        if ('commission-edit' in request.POST):
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
        elif ('job-create' in request.POST):
            jform = JobForm(request.POST)
            if jform.is_valid():
                j = Job()
                j.commission = self.get_object()
                j.role = request.POST.get('role')
                j.manpowerRequired = request.POST.get('manpowerRequired')
                j.save()
                c = self.get_object()
                c.status = 'A'
                c.save()
                return redirect(reverse_lazy('commissions:commission-edit', kwargs={'pk': self.get_object().pk}))
            else:
                print("FORM IS NOT")
                ctx = self.get_context_data(**kwargs)
                ctx['form'] = form
                return self.render_to_response(ctx)
        else:
            ja = JobApplication.objects.get(
                pk=request.POST.get('jobApplication'))
            j = ja.job
            ja.status = 'B' if ('job-accept' in request.POST) else 'C'
            accepted = 0
            ja.save()
            for applicant in JobApplication.objects.filter(job=j, status='B'):
                accepted += 1
            if (accepted >= j.manpowerRequired):
                j.status = 'B'
            j.save()

            full = True
            for job in Job.objects.filter(commission=self.get_object()):
                if (job.status != 'B'):
                    full = False
            if (full):
                c = self.get_object()
                if (c.status == 'A'):
                    c.status = 'B'
                c.save()

            return redirect(reverse_lazy('commissions:commission-edit', kwargs={'pk': self.get_object().pk}))

    def get_success_url(self):
        return reverse_lazy('commissions:commission-detail', kwargs={'pk': self.get_object().pk})


class CommissionCreateView(LoginRequiredMixin, TemplateView):
    '''
    Create view for the Commission model

    Allows users to create new commissions and
    Allows users to optionally create a job with the commission
    '''
    model = Commission
    template_name = 'commissions/commission_add.html'

    def get_context_data(self, **kwargs):
        '''adds context for two forms'''
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = CommissionForm()
        ctx['job_form'] = JobForm()
        return ctx

    def post(self, request, *args, **kwargs):
        '''
        creates commission
        also optionally creates a job if its filled out 
        '''
        form = CommissionForm(request.POST)
        jform = JobForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.author = self.request.user.profile
            c.save()

            if (jform.is_valid() and request.POST.get('role') != ''):
                j = jform.save(commit=False)
                j.commission = c
                j.save()

            return redirect(reverse_lazy('commissions:commission-detail', kwargs={'pk': c.pk}))
        else:
            print("FORM IS NOT")
            ctx = self.get_context_data(**kwargs)
            ctx['form'] = form
            return self.render_to_response(ctx)
