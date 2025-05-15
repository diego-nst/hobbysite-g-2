from django.contrib.auth.forms import UserCreationForm
from user_management.models import Profile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']