from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . models import Notification
from . serializers import NotificationSerializer
from rest_framework.decorators import api_view, permission_classes
from . datasets import NOTIFICATION_CATEGORIES

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

            notifications_list = Notification.objects.filter(destinatary=user)
            notifications_count = notifications_list.count()
            
            if notifications_count < 1:
                return Response({'error': 'No notifications were found'}, status=HTTP_404_NOT_FOUND)
            
            latest_notifications = notifications_list[:5]

            serialied_notifications_list = NotificationSerializer(latest_notifications, many=True)
            return Response({'notifications':serialied_notifications_list.data, 'notifications_count':notifications_count}, status=HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Unexpected error: {e}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
            Create a Notification instance on DB.
        """
        title = request.data.get('title')
        description = request.data.get('description')
        category = request.data.get('category')

        try:
            notification = Notification.objects.create(destinatary=request.user, title=title, description=description, category=category, is_read=False)
            notification.save()
            serialized_notification = NotificationSerializer(notification)
            return Response({'notification':serialized_notification.data, 'message':'Notification created'}, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Unexpected error: {e}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)