from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, ArticleCategory
from .forms import BlogForm, CommentForm, ArticleImageForm
from django.urls import reverse_lazy
from django.shortcuts import redirect



from .models import Article

# Create your views here.


class BlogListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'blog_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            category_dict = dict()
            for category in ArticleCategory.objects.all():
                articles = []
                for article in category.blog.exclude(author=self.request.user.profile):
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



class BlogDetailView(DetailView):
    model = Article
    template_name = 'blog_detail.html'

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'pk': self.get_object().pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['read_more'] = Article.objects.filter(
            author=self.object.author).exclude(pk=self.object.pk)
        ctx['comment_form'] = CommentForm
        ctx['image_form'] = ArticleImageForm
        return ctx
    

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        image_form = ArticleImageForm(request.POST, request.FILES)
        if comment_form.is_valid() or image_form.is_valid:
            if comment_form.is_valid():
                comment_form.instance.author = self.request.user.profile
                comment_form.instance.article = self.get_object()
                comment_form.save()
            if image_form.is_valid():
                article_image = image_form.save(commit=False)
                article_image.article = self.get_object()
                article_image.save()
            return redirect(self.get_success_url())
        else:
            self.object_list = self.get_queryset(**kwargs)
            ctx = self.get_context_data(**kwargs)
            comment_form = CommentForm(request.POST)
            image_form = ArticleImageForm(request.POST, request.FILES)
            return self.render_to_response(ctx) 



class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'blog_create.html'
    form_class = BlogForm

    def get_success_url(self):
        return reverse_lazy('blog:article_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = "blog_update.html"
    form_class = BlogForm

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'pk': self.get_object().pk})