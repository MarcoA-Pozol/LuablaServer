from django.urls import path
from . import views

urlpatterns = [
    ('getFlashcardSchemas', views.get_flashcard_schemas, name='get_flashcard_schemas'),
]