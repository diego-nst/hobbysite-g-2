from django.urls import path
from .views import DashboardView, UpdateProfile
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('profile/dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile/<slug:slug>', UpdateProfile.as_view(), name='profile-update' )
]

app_name = "user_management"
