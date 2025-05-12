from django.shortcuts import render
from wiki.models import Article as Wikis
from blog.models import Article as Blogs
from commissions.models import Commission
from forum.models import Thread
from merchstore.models import Product

def index(request):
    latest_wikis = Wikis.objects.all()[:5]
    latest_blogs = Blogs.objects.all()[:5]
    latest_commisions = Commission.objects.all()[:5]
    latest_threads = Thread.objects.all()[:5]
    latest_products = Product.objects.all()[:5]
    context = {
        'latest_wikis': latest_wikis,
        'latest_blogs': latest_blogs,
        'latest_commisions': latest_commisions,
        'latest_threads': latest_threads,
        'latest_products': latest_products
    }
    return render(request, 'home.html', context)
