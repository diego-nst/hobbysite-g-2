from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article
from .forms import WikiForm
from django.urls import reverse_lazy
from django.shortcuts import redirect


class WikiListView(ListView):
    model = Article
    template_name = 'wiki_list.html'


class WikiDetailView(DetailView):
    model = Article
    template_name = 'wiki_detail.html'


class WikiCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'wiki_create.html'
    form_class = WikiForm

    def get_success_url(self):
        return reverse_lazy('wiki:wiki_list')


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = "wiki_update.html"
    form_class = WikiForm

    def get_success_url(self):
        return reverse_lazy('wiki:wiki_detail', kwargs={'pk': self.get_object().pk})
