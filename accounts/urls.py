from django.urls import path, include
from .views import RegisterView


urlpatterns = [
    path('accounts/register', RegisterView.as_view(), name='register'),
]

app_name = "accounts"
