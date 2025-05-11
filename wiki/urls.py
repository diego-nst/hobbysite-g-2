from django.urls import path
from .views import WikiListView, WikiDetailView, WikiCreateView, WikiUpdateView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/articles', WikiListView.as_view(), name='wiki_list'),
    path('wiki/article/<int:pk>', WikiDetailView.as_view(), name='wiki_detail'),
    path('wiki/article/add', WikiCreateView.as_view(), name='wiki_create'),
    path('wiki/article/<int:pk>/edit',
         WikiUpdateView.as_view(), name='wiki_update'),
]

app_name = "wiki"
