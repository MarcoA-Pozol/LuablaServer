from django.urls import path
from . import views

urlpatterns = [
    path('notifications', views.NotificationsView.as_view(), name='notifications'),
    path('notifications/all', views.fetch_all_notifications, name='all_notifications'),
]