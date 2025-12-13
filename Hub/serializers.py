from . models import Post, PostComment
from rest_framework.serializers import ModelSerializer, ReadOnlyField, SerializerMethodField
from django.core.exceptions import ValidationError
from Authentication.models import User

class PostCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'opinion', 'speech', 'image']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def validate(self, attrs):
        opinion = attrs.get('opinion')
        speech = attrs.get('speech')

        if not opinion and not speech:
            raise ValidationError('You must provide either a text opinion or an audio opinion.')
        return attrs

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
        fields = ['title', 'comment', 'speech', 'image']

    def create(self, validated_data):
        return PostComment.objects.create(**validated_data)

    def validate(self, attrs):
        comment = attrs.get('comment')
        speech = attrs.get('speech')

        if not comment and not speech:
            raise ValidationError('You must provide either comment or an audio comment.')
        return attrs
    
class CommentAuthorSerializer(ModelSerializer):
    profilePicture = SerializerMethodField()
    
    class Meta:
        model = User  
        fields = ['id', 'username', 'profilePicture']
    
    def get_profilePicture(self, obj):
        return str(obj.profile_picture) if obj.profile_picture else None

class PostCommentSerializer(ModelSerializer):
    author = CommentAuthorSerializer()
    
    class Meta:
        model = PostComment 
        fields = ['id', 'author', 'opinion', 'speech', 'image', 'created_at']

class PostAuthorSerializer(ModelSerializer):
    profilePicture = SerializerMethodField()
    
    class Meta:
        model = User  
        fields = ['id', 'username', 'profilePicture']
    
    def get_profilePicture(self, obj):
        return obj.profile_picture.url if hasattr(obj.profile_picture, 'url') else obj.profile_picture
    
class PostResponseSerializer(ModelSerializer):
    author = PostAuthorSerializer()
    comments = PostCommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'language', 'author', 'title', 'opinion', 'speech', 'image', 'created_at', 'comments']