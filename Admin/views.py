from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdmin
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def get_flashcard_schemas(request):
    try:
        schema = {}
        app_config = apps.get_app_config('Flashcards')  

        for model in app_config.get_models():
            model_name = model.__name__
            fields = []

            for field in model._meta.get_fields():
                if hasattr(field, 'get_internal_type'):
                    fields.append({
                        'name': field.name,
                        'type': field.get_internal_type(),
                        'null': getattr(field, 'null', None),
                        'default': field.default if field.default != field.empty else None,
                        'related_model': field.related_model.__name__ if hasattr(field, 'related_model') and field.related_model else None,
                    })

            schema[model_name] = fields
        
        return Response({'schema':schema}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':f'Unexpected error:{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)