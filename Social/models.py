from django.db import models
from Authentication.models import User
from . datasets import NOTIFICATION_CATEGORIES

class Notification(models.Model):
    destinatary = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications', null=False)
    title = models.CharField(max_length=50, default='Hi, recent updates here', null=False)
    description = models.TextField(default="", null=False)
    category = models.CharField(max_length=20, choices=NOTIFICATION_CATEGORIES, default='SYSTEM', null=False)
    is_read = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['destinatary', 'is_read']),
            models.Index(fields=['created_at']),
            models.Index(fields=['category']),
        ]
        db_table = 'Notifications'

    @property
    def get_category_label(self):
        """Frontend can access to the human-readable value for notification.category"""
        return dict(NOTIFICATION_CATEGORIES).get(self.category)
    
    @property
    def get_read_status(self):
        """Return Read | Unread instead of True | False to is_read field"""
        return "Read" if self.is_read == True else "Unread"

    def __str__(self):
        return f'{self.title} - {self.destinarary.username}'