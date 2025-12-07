from django.db import models
from Authentication.models import User
from . validators import validate_audio_file, validate_image_file
from Luabla.models import BaseModel

class Post(BaseModel):
    title = models.CharField(max_length=150, null=False)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, db_index=True, null=False)
    opinion = models.TextField(blank=True, null=True)
    speech = models.FileField(upload_to='post_audios/', blank=True, null=True, validators=[validate_audio_file]) 
    image = models.FileField(upload_to='post_images/', blank=True, null=True, validators=[validate_image_file]) 

class PostComment(BaseModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, db_index=True, null=False)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, db_index=True, null=False)
    comment = models.TextField(blank=True, null=True)
    speech = models.FileField(upload_to='comment_audios/', blank=True, null=True, validators=[validate_audio_file])
    image = models.FileField(upload_to='comment_images/', blank=True, null=True, validators=[validate_image_file]) 