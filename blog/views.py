from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Article

# Create your views here.

class BlogListView(ListView):

    model = Article
    template_name = 'blog_list.html'

class BlogDetailView(DetailView):

    model = Article
    template_name = 'blog_detail.html'

