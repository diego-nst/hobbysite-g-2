from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from commissions.models import Commission, JobApplication
from blog.models import Article as BlogArticle
from merchstore.models import Product, ProductType, Transaction
from forum.models import Thread
from wiki.models import Article as WikiArticle
from .models import Profile
from .forms import ProfileForm

def index(request):
    latest_wikis = WikiArticle.objects.all()[:5]
    latest_blogs = BlogArticle.objects.all()[:5]
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


class UpdateProfile(UpdateView, LoginRequiredMixin):
    model = Profile
    form = ProfileForm
    template_name = "user_management/profile.html"
    fields = ['display_name']

    def get_success_url(self):
        return reverse_lazy('user_management:dashboard')
    
    def get_context_data(self, **kwargs):

        return super().get_context_data(**kwargs)
    
    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(slug=slug)
        return context

class DashboardView(TemplateView, LoginRequiredMixin):
    template_name = "user_management/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if (self.request.user.is_authenticated):
            user_cart = dict()
            for transaction in self.request.user.profile.transactions.all():
                if transaction.product.owner in user_cart:
                    user_cart[transaction.product.owner].append(transaction)
                else:
                    user_cart[transaction.product.owner] = [transaction]
            seller_transactions = dict()
            for transaction in Transaction.objects.all():
                if transaction.product.owner==self.request.user.profile:
                    if transaction.buyer in seller_transactions:
                        seller_transactions[transaction.buyer].append(transaction)
                    else:
                        seller_transactions[transaction.buyer] = [transaction]
            ctx['seller_transactions'] = seller_transactions
            ctx['user_cart'] = user_cart
            ctx['blog_articles'] = BlogArticle.objects.filter(
                author=self.request.user.profile)
            ctx['user_threads'] = Thread.objects.filter(
                author=self.request.user.profile)
            ctx['wiki_articles'] = WikiArticle.objects.filter(
                author=self.request.user.profile)
            applied = set()
            for application in JobApplication.objects.filter(applicant=self.request.user.profile):
                applied.add(application.job.commission)
            ctx['created_commissions'] = Commission.objects.filter(
                author=self.request.user.profile)
            ctx['applied_commissions'] = applied

        return ctx
