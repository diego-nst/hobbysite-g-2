from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, ArticleCategory
from .forms import WikiForm, CommentForm
from django.urls import reverse_lazy
from django.shortcuts import redirect


class WikiListView(ListView):
    model = ArticleCategory
    template_name = 'wiki_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            category_dict = dict()
            for category in ArticleCategory.objects.all():
                articles = []
                for article in category.articles.exclude(author=self.request.user.profile):
                    articles.append(article)
                category_dict[category] = articles
            ctx['user_articles'] = Article.objects.filter(
                author=self.request.user.profile)
            ctx['other_articles'] = category_dict

        else:
            category_dict = dict()
            for category in ArticleCategory.objects.all():
                list = []
                for article in category.articles.all():
                    list.append(article)
                category_dict[category] = list
            ctx['other_articles'] = category_dict
        return ctx


class WikiDetailView(DetailView):
    model = Article
    template_name = 'wiki_detail.html'

    def get_success_url(self):
        return reverse_lazy('wiki:wiki_detail', kwargs={'pk': self.get_object().pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['read_more'] = Article.objects.filter(
            category=self.object.category).exclude(pk=self.object.pk)
        ctx['form'] = CommentForm
        return ctx

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = self.request.user.profile
            form.instance.article = self.get_object()
            form.save()
            return redirect(self.get_success_url())

        else:
            ctx = self.get_context_data(**kwargs)
            ctx['form'] = form
            return self.render_to_response(ctx)


class WikiCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'wiki_create.html'
    form_class = WikiForm

    def get_success_url(self):
        return reverse_lazy('wiki:wiki_list')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class WikiUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = "wiki_update.html"
    form_class = WikiForm

    def get_success_url(self):
        return reverse_lazy('wiki:wiki_detail', kwargs={'pk': self.get_object().pk})
