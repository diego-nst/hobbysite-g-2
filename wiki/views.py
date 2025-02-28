from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Article


class WikiListView(ListView):
    model = Article
    template_name = 'site_list.html'


class WikiDetailView(DetailView):
    model = Article
    template_name = 'site_detail.html'