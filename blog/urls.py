from django.urls import path



from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView

urlpatterns = [
    path('articles', BlogListView.as_view(), name='article_list'),
    path('article/<int:pk>', BlogDetailView.as_view(), name='article_detail'),
    path('article/add', BlogCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/update', BlogUpdateView.as_view(), name='article_update')
]


app_name = 'ledger'
