from django.urls import path
from .views import ThreadDetailView, ThreadListView

urlpatterns = [
    path('forum/threads', ThreadListView.as_view(), name='list'),
    path('forum/thread/1', ThreadDetailView.as_view(), name='thread_detail')
]

app_name = 'forum'
'''List View: /forum/threads
Detail View: /forum/thread/1
'''