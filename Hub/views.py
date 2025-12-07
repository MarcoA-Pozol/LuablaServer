from . models import Post
from . serializers import PostResponseSerializer, PostCreateUpdateSerializer, PostCommentResponseSerializer, PostCommentCreateUpdateSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_posts(request):
    language = request.data.get('language')
    
    posts = Post.objects.filter(language=language).all()
    serialized_posts = PostResponseSerializer(posts, many=True)

    return Response({'items':serialized_posts}, status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_posts_by_user_id(request):
    language = request.data.get('language')
    user = request.user
    
    posts = PostResponseSerializer(Post.objects.filter(language=language, author=user), many=True)
    
    return Response({'items':posts}, status=HTTP_200_OK)
    

class PostView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get post by post id"""
        try:
            post_id = request.query_params.get('id')
            
            post = PostResponseSerializer(Post.objects.get(id=post_id))
            
            return Response({'item':post}, status=HTTP_200_OK)
        except Exception as e:
            return Response({'error':e}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Create post by request body"""
        serializer = PostCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            new_item = serializer.save(author=request.user)

            serialized_item = PostResponseSerializer(new_item)
            item = serialized_item.data
            
            return Response({'item':item}, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            post_id = request.query_params.get('id')
            
            post = Post.objects.get(id=post_id)
            post.delete()
            
            return Response({'item':post}, status=HTTP_200_OK)
        except Exception as e:
            return Response({'error':e}, status=HTTP_500_INTERNAL_SERVER_ERROR)