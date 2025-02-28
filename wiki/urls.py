from django.urls import path
from .views import WikiListView, WikiDetailView


urlpatterns = [
    path('wiki/article', WikiListView.as_view(), name='article_list'),
    path('wiki/article/<int:pk>', WikiDetailView.as_view(), name='article_detail')
]

app_name = "wiki"
