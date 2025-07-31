from rest_framework.serializers import ModelSerializer, CharField
from . models import Notification

class NotificationSerializer(ModelSerializer):
    category_label = CharField(source='get_category_label', read_only=True)
    read_status = CharField(source='get_read_status', read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'