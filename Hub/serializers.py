from . models import Post, PostComment
from rest_framework.serializers import ModelSerializer, ReadOnlyField

# Post
class PostResponseSerializer(ModelSerializer):
    author_username = ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'author_username', 'comment', 'speech', 'image']

class PostCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'opinion', 'speech', 'image']

# Post Comment
class PostCommentResponseSerializer(ModelSerializer):
    post_title = ReadOnlyField(source='post.title')
    author_username = ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'post_title', 'author_username', 'comment', 'speech', 'image']

class PostCommentCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'opinion', 'speech', 'image']