from django.urls import path
from . import views

urlpatterns = [
    path('notifications', views.NotificationsView.as_view(), name='notifications'),
    path('notifications/all', views.fetch_all_notifications, name='all_notifications'),
    path('notifications/categoriesList', views.fetch_notifications_categories_list, name='notifications_categories'),
    path('notifications/toggleReadStatus', views.toggle_notification_read_status, name='toggle_notification_read_status'),
]