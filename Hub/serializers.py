from . models import Post, PostComment
from rest_framework.serializers import ModelSerializer, ReadOnlyField, SerializerMethodField, PrimaryKeyRelatedField
from django.core.exceptions import ValidationError
from Authentication.models import User

class PostCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'opinion', 'speech', 'image', 'language']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def validate(self, attrs):
        opinion = attrs.get('opinion')
        speech = attrs.get('speech')

        if not opinion and not speech:
            raise ValidationError('You must provide either a text opinion or an audio opinion.')
        return attrs

# Post Comment
class CommentAuthorResponseSerializer(ModelSerializer):
    profile_picture = SerializerMethodField()
    
    class Meta:
        model = User  
        fields = ['id', 'username', 'profile_picture']
    
    def get_profile_picture(self, obj):
        return str(obj.profile_picture) if obj.profile_picture else None


class PostCommentResponseSerializer(ModelSerializer):
    author = CommentAuthorResponseSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'author', 'comment', 'speech', 'image', 'created_at']

    def get_image(self, obj):
        return str(obj.image) if obj.image else None

class PostCommentCreateUpdateSerializer(ModelSerializer):
    post_id = PrimaryKeyRelatedField(
        queryset=Post.objects.all()
    )

    class Meta:
        model = PostComment
        fields = ['post_id', 'comment', 'speech', 'image']

    def validate(self, attrs):
        comment = attrs.get('comment')
        speech = attrs.get('speech')

        if not comment and not speech:
            raise ValidationError('You must provide either comment or an audio comment.')
        return attrs
    
class CommentAuthorSerializer(ModelSerializer):
    profile_picture = SerializerMethodField()
    
    class Meta:
        model = User  
        fields = ['id', 'username', 'profile_picture']
    
    def get_profile_picture(self, obj):
        return str(obj.profile_picture) if obj.profile_picture else None

class PostCommentSerializer(ModelSerializer):
    author = CommentAuthorSerializer()
    
    class Meta:
        model = PostComment 
        fields = ['id', 'author', 'comment', 'speech', 'image', 'created_at']

class PostAuthorSerializer(ModelSerializer):
    profile_picture = SerializerMethodField()
    
    class Meta:
        model = User  
        fields = ['id', 'username', 'profile_picture']
    
    def get_profile_picture(self, obj):
        return obj.profile_picture.url if hasattr(obj.profile_picture, 'url') else obj.profile_picture
    
class PostResponseSerializer(ModelSerializer):
    author = PostAuthorSerializer()
    comments = PostCommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'language', 'author', 'title', 'opinion', 'speech', 'image', 'created_at', 'comments']