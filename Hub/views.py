from . models import Post
from . serializers import PostResponseSerializer, PostCreateUpdateSerializer, PostCommentResponseSerializer, PostCommentCreateUpdateSerializer
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from . throttles import ListPostsByLanguageThrottle
from Luabla.decorators import manage_exceptions
from Luabla.mixins import ExceptionHandlerAPIView

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([ListPostsByLanguageThrottle])
def list_posts_by_language(request):
    """Get all posts by language. All posts from other users."""
    language = request.GET.get('language')
    
    posts = Post.objects.filter(language=language).order_by('-created_at')

    paginator = PageNumberPagination()
    paginator.page_size = 10 

    paginated_posts = paginator.paginate_queryset(posts, request)

    serialized_posts = PostResponseSerializer(paginated_posts, many=True)
    
    posts = serialized_posts.data

    return Response({'items':posts}, status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@manage_exceptions
def list_posts_by_user(request):
    """Get all posts of a language from the auth user."""
    language = request.GET.get('language')
    user = request.user
    
    serialized_posts = PostResponseSerializer(Post.objects.filter(language=language, author=user), many=True)
    posts = serialized_posts.data
    
    return Response({'items':posts}, status=HTTP_200_OK)
    

class PostView(ExceptionHandlerAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get post by post id"""
        post_id = request.query_params.get('id')
        
        post = PostResponseSerializer(Post.objects.get(id=post_id))
        
        return Response({'item':post}, status=HTTP_200_OK)

    def post(self, request):
        """Create post by request body"""
        serializer = PostCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            new_item = serializer.save(author=request.user)

            serialized_item = PostResponseSerializer(new_item)
            item = serialized_item.data
            
            return Response({'item':item}, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        """Update post values completely"""
        post_id = request.query_params.get('id')
        if not post_id:
            return Response({'error': 'Missing id'}, status=400)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)

        serializer = PostCreateUpdateSerializer(
            post,
            data=request.data, 
            partial=False 
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'item': serializer.data}, status=200)
        
        return Response(serializer.errors, status=400)

    def patch(self, request):
        """Update post's values partially"""
        post_id = request.query_params.get('id')
        if not post_id:
            return Response({'error': 'Missing id'}, status=400)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)

        serializer = PostCreateUpdateSerializer(
            post,
            data=request.data,
            partial=True  
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'item': serializer.data}, status=200)
            
        return Response(serializer.errors, status=400)

    def delete(self, request):
        """Delete post from database"""
        post_id = request.query_params.get('id')
        
        post = Post.objects.get(id=post_id)
        post.delete()
        
        return Response({'item':post}, status=HTTP_200_OK)