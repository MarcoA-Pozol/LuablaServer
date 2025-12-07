from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR


class ExceptionHandlerAPIView(APIView):
    """Manages exceptions for endpoints based on APIView class"""
    def handle_exception(self, exc):
        return Response({'error': str(exc)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
