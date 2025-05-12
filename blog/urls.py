from django.urls import path



from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView

urlpatterns = [
    path('blog/articles', BlogListView.as_view(), name='article_list'),
    path('blog/article/<int:pk>', BlogDetailView.as_view(), name='article_detail'),
    path('blog/article/add', BlogCreateView.as_view(), name='article_create'),
    path('blog/article/<int:pk>/update', BlogUpdateView, name='article_update')
]


app_name = 'ledger'
