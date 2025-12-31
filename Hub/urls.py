from django.urls import path
from . import views

urlpatterns = [
    path('posts/all', views.list_posts_by_language, name='list_all_posts'),
    path('posts', views.list_posts_by_user, name='list_posts_by_user'),
    path('post', views.PostView.as_view(), name='post'),
    path('postComment', views.PostCommentView.as_view(), name='post_comment')
]