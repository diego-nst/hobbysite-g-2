from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse
from django.shortcuts import redirect

from .models import Product, ProductType, Transaction
from .forms import CreateTransactionForm, CreateProductForm, UpdateProductForm, UpdateTransactionStatusForm
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
                    else:
                        products_dict[pt] += [product]

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
            t.status = 'Available'
            if ((t.amount <= 0)):
                print('Error. At least one item must be added to cart.')
            if ((t.product.stock - t.amount) < 0):
                print('Error. The quantity given is creater than the remaining stock')
            else:
                t.product.stock = t.product.stock - t.amount
                if (t.product.stock == 0):
                    t.product.status = 'Out of stock'
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateProductForm
        context['product_types'] = ProductType.objects.all()
        context['status_choices'] = Product.STATUS_CHOICES
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)
        # used https://stackoverflow.com/questions/65733442/in-django-how-to-add-username-to-a-model-automatically-when-the-form-is-submit

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'productUpdate.html'
    form_class = UpdateProductForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['pk'] = pk
        context['product'] = Product.objects.get(pk=pk)
        context['product_types'] = ProductType.objects.all()
        context['status_choices'] = Product.STATUS_CHOICES
        return context

    def form_valid(self, form):
        if form.instance.stock <= 0:
            form.instance.status = 'Out of stock'
        else:
            form.instance.status = 'Available'
        return super().form_valid(form)


class CartView(LoginRequiredMixin, ListView):
    model = Transaction

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
        context['form'] = UpdateTransactionStatusForm
        seller_transactions = dict()
        if self.request.user.is_authenticated:
            for transaction in Transaction.objects.all():
                if transaction.product.owner == self.request.user.profile:
                    if transaction.buyer in seller_transactions:
                        seller_transactions[transaction.buyer].append(
                            transaction)
                    else:
                        seller_transactions[transaction.buyer] = [transaction]
        context['seller_transactions'] = seller_transactions
        context['status_choices'] = Transaction.STATUS_CHOICES
        return context

    template_name = 'transactionList.html'


class TransactionDetailView(LoginRequiredMixin, UpdateView):
    model = Transaction
    template_name = 'transactionDetail.html'
    form_class = UpdateTransactionStatusForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['pk'] = pk
        context['form'] = UpdateTransactionStatusForm()
        context['transaction'] = Transaction.objects.get(pk=pk)
        context['status_choices'] = Transaction.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = UpdateTransactionStatusForm(
            request.POST, instance=Transaction.objects.get(pk=pk))

        t = form.save(commit=False)
        t.status = request.POST.get('status')
        t.save()
        return redirect(reverse('merchstore:transactions-list'))
