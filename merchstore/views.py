from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# remove these?
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect

from .models import Product, ProductType, Transaction
from .forms import CreateTransactionForm, CreateProductForm, UpdateProductForm
from user_management.models import Profile


class ProductListView(ListView):
    model = ProductType
    template_name = 'productList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_is_selling = False
        user_products_dict = dict()
        products_dict = dict()

        if self.request.user.is_authenticated:
            for pt in ProductType.objects.all():

                products_dict[pt] = list()
                user_products_dict[pt] = list()

                for product in pt.get_products():
                    if (product.owner == self.request.user.profile):
                        user_products_dict[pt] += [product]
                        print('user_products_dict was appended with ' + product.name)
                    else:
                        products_dict[pt] += [product]
                        print('products_dict was appended with ' + product.name)

                if len(user_products_dict[pt]) == 0:
                    del user_products_dict[pt]
                else:
                    user_is_selling = True
                if len(products_dict[pt]) == 0:
                    del products_dict[pt]

            context['owned_by_user'] = user_products_dict
            context['user_can_buy'] = products_dict

        else:
            products_dict = {pt: [p for p in pt.get_products()]
                             for pt in ProductType.objects.all()}
            context['user_can_buy'] = products_dict

        context['user_is_selling'] = user_is_selling
        context['form'] = CreateTransactionForm()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'productDetail.html'
    form_class = CreateTransactionForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['pk'] = pk
        context['form'] = CreateTransactionForm()
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = CreateTransactionForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.buyer = self.request.user.profile
            t.product = Product.objects.get(pk=pk)
            t.status = 'IN_CART'
            if ((t.amount <= 0)):
                print('Error. At least one item must be added to cart.')
            if ((t.product.stock - t.amount) < 0):
                print('Error. The quantity given is creater than the remaining stock')
            else:
                t.product.stock = t.product.stock - t.amount
                if (t.product.stock == 0):
                    t.product.status = 'NO_STOCK'
            t.product.save()
            t.save()
            return redirect(reverse('merchstore:cart'))
        else:
            print('The Transaction form submission was invalid.')
            print(form.errors)
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'productCreate.html'
    form_class = CreateProductForm

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)
        # used https://stackoverflow.com/questions/65733442/in-django-how-to-add-username-to-a-model-automatically-when-the-form-is-submit


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'productUpdate.html'
    form_class = UpdateProductForm

    def form_valid(self, form):
        if form.instance.stock <= 0:
            form.instance.status = 'NO_STOCK'
        else:
            form.instance.status = 'AVAILABLE'
        return super().form_valid(form)


class CartView(LoginRequiredMixin, ListView):
    model = Transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_cart = dict()
        products_in_cart = dict()
        if self.request.user.is_authenticated:
            for transaction in self.request.user.profile.transactions.all():
                if transaction.product.owner in user_cart:
                    user_cart[transaction.product.owner].append(transaction)
                else:
                    user_cart[transaction.product.owner] = [transaction]
                products_in_cart.add(transaction.product)

        context['user_cart'] = user_cart
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_cart = dict()
        if self.request.user.is_authenticated:
            for transaction in self.request.user.profile.transactions.all():
                if transaction.product.owner in user_cart:
                    user_cart[transaction.product.owner].append(transaction)
                else:
                    user_cart[transaction.product.owner] = [transaction]

        context['user_cart'] = user_cart
        return context

    template_name = 'cart.html'


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller_transactions = dict()

        if self.request.user.is_authenticated:
            for transaction in self.request.user.profile.transactions.all():
                if transaction.buyer in seller_transactions:
                    seller_transactions[transaction.buyer].append(transaction)
                    print("a")
                else:
                    seller_transactions[transaction.buyer] = [transaction]
                    print("b")
                    print(transaction.buyer.display_name)
        context['seller_transactions'] = seller_transactions
        return context

    template_name = 'transactionList.html'
