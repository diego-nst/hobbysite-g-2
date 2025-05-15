from django.urls import path



from .views import CreateUser

urlpatterns = [
    path('accounts/register', CreateUser.as_view(), name='register_user')
]


app_name = 'ledger'