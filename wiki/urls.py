from django.urls import path
from .views import WikiListView, WikiDetailView, WikiCreateView


urlpatterns = [
    path('wiki/articles', WikiListView.as_view(), name='article_list'),
    path('wiki/article/<int:pk>', WikiDetailView.as_view(), name='article_detail'),
    path('wiki/article/add', WikiCreateView.as_view(), name='wiki_create'),
    path('wiki/article/<int:pk>/edit',
         RecipeUpdateView.as_view(), name='recipe_update'),
]

app_name = "wiki"
