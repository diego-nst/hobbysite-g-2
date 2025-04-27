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


class ProductDetailView(DetailView):
    model = Product
    template_name = "product.html"
    form_class = CreateTransactionForm

    # def get_context_data(self, **kwargs):
    #     pk = self.kwargs['pk']
    #     ctx = super().get_context_data(**kwargs)
    #     ctx['form'] = CreateTransactionForm()
    #     ctx['product'] = Product.objects.get(pk=pk)
    #     return ctx

    # def post(self, request, *args, **kwargs):
    #     pk = self.kwargs['pk']
    #     form = CreateTransactionForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         t = Transaction()
    #         t.buyer #HOW DO YOU GET THIS
    #         t.product = Product.objects.get(pk=pk)
    #         t.amount = request.POST.get('amount')
    #         t.created_on = request.POST.get('created_on')
    #         t.save()

    #         return redirect(reverse('merchstore:cart', args=[pk]))

    #     else:
    #         self.object_list = self.get_queryset(**kwargs)
    #         context = self.get_context_data(**kwargs)
    #         context['form'] = form
    #         return self.render_to_response(context)

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

# class CartView(LoginRequiredMixin, ListView):
#     model = Transaction
#     template_name = ""


# class TransactionListView(LoginRequiredMixin, ListView):
#     model = Transaction
#     template_name = ""
