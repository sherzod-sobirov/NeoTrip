from django.urls import path
from .views import DetailPostView, PostListView

urlpatterns = [
    path('post-detail/<int:pk>', DetailPostView.as_view(), name="detail_post"),
    path('post-list/', PostListView.as_view(), name="post_post_list")
]
