from django.shortcuts import render
from .models import Profile
from .forms import CreateUserForm
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
# Create your views here.

class CreateUserView(CreateView):
    model = Profile
    template_name = "accounts/register.html"
    form = CreateUserForm

    def get_success_url(self):
        return reverse_lazy('accounts:register_user')
    
    def post(self):
        form = CreateUserForm
        if form.is_valid():
            form.save()
