from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.list_posts, name='list_posts'),
]