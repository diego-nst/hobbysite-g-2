from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, ArticleCategory
from .forms import WikiForm, CommentForm
from django.urls import reverse_lazy
from django.shortcuts import redirect



from .models import Article

# Create your views here.


class BlogListView(ListView):
    model = Article
    template_name = 'blog_list.html'


class BlogDetailView(DetailView):
    model = Article
    template_name = 'blog_detail.html'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Article
