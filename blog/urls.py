from django.urls import path


from .views import recipe_list_view, recipe_detail_view

urlpatterns = [
    path('blog/articles', recipe_list_view, name='blog_list'),
    path('blog/article/<int:pk>', recipe_detail_view, name='blog_detail'),
]

app_name = 'ledger'