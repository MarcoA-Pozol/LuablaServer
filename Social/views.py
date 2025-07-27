from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . models import Notification
from . serializers import NotificationSerializer

class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
            Fetch user's notifications list.
        """
        try:
            user = request.user
            if not user:
                return Response({'error': 'Not authenticated'}, status=HTTP_401_UNAUTHORIZED)

            notifications_list = Notification.objects.filter(destinatary=user).all()
            if len(notifications_list) < 1:
                return Response({'error': 'No notifications were found'}, status=HTTP_404_NOT_FOUND)

            serialied_notifications_list = NotificationSerializer(notifications_list, many=True)
            return Response({'notifications':serialied_notifications_list}, status=HTTP_200_OK)
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
            return Response({'notification':serialized_notification, 'message':'Notification created'}, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Unexpected error: {e}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)