from django.shortcuts import render
from wiki.models import Article as Wikis

def index(request):
    latest_wikis = Wikis.objects.all()[:3]
    context = {
        'latest_wikis': latest_wikis
    }
    return render(request, 'home.html', context)
