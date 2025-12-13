from django.core.exceptions import ValidationError

def validate_audio_file(value):
    if not value:
        return value
    valid_types = ['audio/mpeg', 'audio/webm', 'audio/wav', 'audio/ogg']
    if value.size > 8 * 1024 * 1024:
        raise ValidationError('Audio file too large (max 10 MB).')
    if value.content_type not in valid_types:
        raise ValidationError('Unsupported audio format.')
    return value
    
def validate_image_file(value):
    if not value:
        return value
    valid_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    if value.size > 6 * 1024 * 1024:
        raise ValidationError('Image file too large (max 6 MB).')
    if value.content_type not in valid_types:
        raise ValidationError('Unsupported image format.')
    return value