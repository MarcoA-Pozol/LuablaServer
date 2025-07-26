from rest_framework.serializers import ModelSerializer, CharField
from . models import Notification

class NotificationSerializer(ModelSerializer):
    category_display = CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'