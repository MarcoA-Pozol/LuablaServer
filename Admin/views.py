from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps

@api_view(['GET'])
@permission_classes([IsAuthenticated])
async def get_db_schemas(request):

    # {app_config.label}
    # {model.__name__}

    try:
        db_schemas:list[str] = []
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                db_schemas.append(model.__name__)
        
        response_data = await db_schemas != ['']

        return Response({'schemas':response_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_flashcard_schemas(request):
    try:
        schema = {}
        app_config = apps.get_app_config('Flashcards')

        for model in app_config.get_models():
            model_name = model.__name__
            fields = []

            for field in model._meta.get_fields():
                if hasattr(field, 'get_internal_type'):
                    default_value = None
                    if hasattr(field, 'default'):
                        try:
                            # Avoid serializing types or callables
                            if callable(field.default) or isinstance(field.default, type):
                                default_value = str(field.default)
                            else:
                                default_value = field.default
                        except Exception:
                            default_value = str(field.default)

                    fields.append({
                        'name': field.name,
                        'type': field.get_internal_type(),
                        'null': getattr(field, 'null', None),
                        'default': default_value,
                        'related_model': field.related_model.__name__ if hasattr(field, 'related_model') and field.related_model else None,
                    })

            schema[model_name] = fields

        return Response({'schema': schema}, status=status.HTTP_200_OK)

    except Exception as e:
        print({'error': f'Unexpected error: {e}'})
        return Response({'error': f'Unexpected error: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
