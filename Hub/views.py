from . models import Post
from . serializers import PostResponseSerializer, PostCreateUpdateSerializer, PostCommentResponseSerializer, PostCommentCreateUpdateSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_posts(request):

    return Response({'item':['This is an empty posts list']}, status=HTTP_200_OK)