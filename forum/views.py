from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy

from .models import Thread, ThreadCategory
from .forms import ThreadForm, CommentForm


class ThreadListView(ListView):
    model = Thread
    template_name = 'thread_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_threads'] = Thread.objects.filter(
                author=self.request.user.profile)
            context['other_threads'] = Thread.objects.exclude(
                author=self.request.user.profile)
        context['thread_categories'] = ThreadCategory.objects.all()
        return context


class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'thread_detail.html'

    def get_success_url(self):
        return reverse_lazy('forum:thread_detail', kwargs={'pk': self.get_object().pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['loggedin_user'] = self.request.user.profile
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = self.request.user.profile
            form.instance.thread = self.get_object()
            form.save()
            return redirect(self.get_success_url())
        else:
            print("Error in posting form")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = 'thread_form.html'

    def get_success_url(self):
        # return reverse_lazy('forum:thread_detail', kwargs={'pk': self.object.pk})
        return reverse_lazy('forum:thread_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ThreadForm()
        return context

    def post(self, request, *awgs, **kwargs):
        form = self.get_form(ThreadForm)
        if form.is_valid():
            form.instance.author = self.request.user.profile
            form.save()
            return redirect(self.get_success_url())
        else:
            print("Error in posting form")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class ThreadUpdateView(LoginRequiredMixin, UpdateView):
    model = Thread
    form_class = ThreadForm
    # form_class = ThreadUpdateForm
    template_name = 'thread_form.html'

    def get_success_url(self):
        return reverse_lazy('forum:thread_detail', kwargs={'pk': self.object.pk})
