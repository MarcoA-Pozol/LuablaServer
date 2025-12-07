from django.urls import path
from . import views

urlpatterns = [
    path('posts/all', views.list_posts, name='list_all_posts'),
    path('posts', views.list_posts_by_user_id, name='list_posts'),
    path('post', views.create_post, name='create_post'),
]