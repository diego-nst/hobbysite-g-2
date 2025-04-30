from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# remove these?
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect

from .models import Product, ProductType, Transaction
from .forms import CreateTransactionForm, CreateProductForm, UpdateProductForm


class ProductListView(ListView):
    model = ProductType
    template_name = "productList.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user_is_selling = False
        user_products_dict = dict()
        products_dict = dict()

        if self.request.user.is_authenticated:
            for pt in ProductType.objects.all():
                products_dict[pt] = []
                user_products_dict[pt] = []
                for p in pt.get_products():
                    if (p.owner==self.request.user.profile):
                        user_products_dict[pt].append(p)
                    else:
                        products_dict[pt].append(p)
                if len(products_dict[pt]) != 0:
                    user_is_selling = True
            context['owned_by_user'] = user_products_dict
            context['user_can_buy'] = products_dict
        
        else:
            products_dict = {pt:[p for p in pt.get_products()] for pt in ProductType.objects.all()}
            context['user_can_buy'] = products_dict

        print("The user is selling an item: " + str(user_is_selling))
        print("Length of owned_by_user: " + str(len(user_products_dict)))
        print("Length of products_dict: " + str(len(products_dict)))

        context['owned_by_user'] = user_products_dict
        context['form'] = CreateTransactionForm()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "product.html"
    form_class = CreateTransactionForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['form'] = CreateTransactionForm()
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = CreateTransactionForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.buyer = self.request.user.profile
            t.product = Product.objects.get(pk=pk)
            t.status = "IN_CART"
            if ((t.product.stock - t.amount) < 0):
                print("Please input a number greater than or equal to the remaining stock.")
                # im thinking of having this message show up on the webpage
            else:
                t.product.stock = t.product.stock - t.amount
                if (t.product.stock==0):
                    t.product.status = "NO_STOCK"
            t.product.save()
            t.save()
            return self.get(request, *args, **kwargs)
        else:
            print("The Transaction form submission was invalid.")
            print(form.errors)
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "productCreate.html"
    form_class = CreateProductForm

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)
        # used https://stackoverflow.com/questions/65733442/in-django-how-to-add-username-to-a-model-automatically-when-the-form-is-submit


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "productUpdate.html"
    form_class = UpdateProductForm

    def form_valid(self, form):
        if form.instance.stock <= 0:
            form.instance.status = "NO_STOCK"
        else:
            form.instance.status = "AVAILABLE"
        return super().form_valid(form)

class CartView(LoginRequiredMixin, ListView):
    model = Transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_transactions = list()
        if self.request.user.is_authenticated:
            user_transactions = [t for t in Transaction.objects.all() if (t.product.owner==self.request.user.profile)]
            context['user_transactions'] = user_transactions
        print("The number of transactions the user has: " + str(user_transactions))
        context['form'] = CreateTransactionForm()
        return context

    template_name = ""


# class TransactionListView(LoginRequiredMixin, ListView):
#     model = Transaction
#     template_name = ""
