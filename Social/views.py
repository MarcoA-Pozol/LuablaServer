from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . models import Notification
from . serializers import NotificationSerializer
from rest_framework.decorators import api_view, permission_classes
from . datasets import NOTIFICATION_CATEGORIES
from Authentication.models import User

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_notifications_categories_list(request):
    
    user = request.user 

    if not user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=HTTP_401_UNAUTHORIZED)

    try:
        categories_list = [category[1] for category in NOTIFICATION_CATEGORIES] 
        return Response({'categories':categories_list}, status=HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Unexpected error: {e}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_all_notifications(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=HTTP_401_UNAUTHORIZED)

        notifications = Notification.objects.filter(destinatary=user)
        notifications_count = notifications.count()
        serialized_notifications = NotificationSerializer(notifications, many=True)

        return Response({'notifications':serialized_notifications.data, 'notifications_count':notifications_count})
    except Exception as e:
        return Response({'error':f'Unexpected error:{e}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_notification_read_status(request):
    """
        Set a Notification's instance as read or unread based on the boolean toggling.
    """
    try:
        notification_id = request.data.get('notificationId')

        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=HTTP_401_UNAUTHORIZED)
        
        notification = Notification.objects.filter(id=notification_id).first()
        updated_notification = NotificationSerializer(notification)

        if not notification:
            return Response({'error':'Notification was not found'}, status=HTTP_404_NOT_FOUND)

        notification.is_read = not notification.is_read # Toggle booleans
        notification.save()

        return Response({'message':'Notiication was set as read', 'updated_notification':updated_notification.data}, status=HTTP_200_OK)
    except Exception as e:
        return Response({'error':f'Unexpected error:{e}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
            Fetch user's notifications list.
        """
        try:
            user = request.user
            if not user.is_authenticated:
                return Response({'error': 'Not authenticated'}, status=HTTP_401_UNAUTHORIZED)

            notifications = Notification.objects.filter(destinatary=user)
            notifications_count = notifications.count()
            new_notifications = notifications.filter(is_read=False)
            
            if notifications_count < 1:
                return Response({'error': 'No notifications were found'}, status=HTTP_404_NOT_FOUND)
            
            # latest_notifications = notifications_list[:5]

            serialized_notifications_list = NotificationSerializer(notifications, many=True)
            return Response({'notifications':serialized_notifications_list.data, 'notifications_count':notifications_count, 'new_notifications_count':new_notifications.count()}, status=HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Unexpected error: {e}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
            Create a Notification instance on DB.
        """
        title = request.data.get('title')
        description = request.data.get('description')
        category = request.data.get('category')
        destinatary_username = request.data.get('destinatary')
        
        if destinatary_username:
            destinatary = User.objects.get(username=destinatary_username)
        else:
            destinatary = request.user

        try:
            notification = Notification.objects.create(destinatary=destinatary, title=title, description=description, category=category, is_read=False)
            notification.save()
            serialized_notification = NotificationSerializer(notification)
            return Response({'notification':serialized_notification.data, 'message':'Notification created'}, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Unexpected error: {e}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)