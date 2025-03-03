from django.shortcuts import render
from .models import Article, ArticleCategory

# Create your views here.

def article_list(request):
    print(request)

    article_categories = ArticleCategory.objects.all()

    ctx = {
        "ArticleCategory": article_categories
    }

    return render(request, "blog_list.html", ctx)

def article_detail(request, pk):
    print(request)

    article = Article.objects.get(pk = pk)

    ctx = {
        "Article": article,
    }

    return render(request, "blog_detail.html", ctx)