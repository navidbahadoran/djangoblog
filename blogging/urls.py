from django.urls import path
from blogging.views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
                            UserPostListView, LatestEntriesFeed, PostCategoryInlineCreateView)

urlpatterns = [
    path('', PostListView.as_view(), name="post-list"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/new/', PostCategoryInlineCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('latest/feed/', LatestEntriesFeed(), name='news-item')
]
