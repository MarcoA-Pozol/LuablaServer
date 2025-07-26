from django.urls import path
from . import views

urlpatterns = [
    path('notifications', views.NotificationsView.as_view(), name='notifications'),
]