from django.urls import path
from .views import DashboardView, UpdateProfile


urlpatterns = [
    path('profile/dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile/<slug:slug>', UpdateProfile.as_view(), name='profil-update' )
]

app_name = "user_management"
