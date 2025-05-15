from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from user_management.models import Profile\


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        Profile.objects.create(
            user=user,
            display_name=user.username,
            email=user.email,
            slug=user.username
        )

        return super().form_valid(form)
