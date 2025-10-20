from django.db import models
from Authentication.models import User
from django.core.exceptions import ValidationError

def validate_audio_file(value):
    valid_types = ['audio/mpeg', 'audio/webm', 'audio/wav']
    if value.size > 10 * 1024 * 1024:
        raise ValidationError("Audio file too large (max 10 MB).")
    if value.file.content_type not in valid_types:
        raise ValidationError("Unsupported audio format.")

class Post(models.Model):
    title = models.CharField(max_length=150, null=False)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, db_index=True, null=False)
    opinion = models.TextField(blank=True, null=True)
    speech = models.FileField(upload_to='post_audios/', blank=True, null=True, validators=[validate_audio_file]) 
    image = models.FileField(upload_to='post_images/', blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class PostComment():
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, db_index=True, null=False)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, db_index=True, null=False)
    comment = models.TextField(blank=True, null=True)
    speech = models.FileField(upload_to='comment_audios/', blank=True, null=True)
    image = models.FileField(upload_to='comment_images/', blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)