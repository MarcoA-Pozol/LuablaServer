from django.urls import path
from . import views

urlpatterns = [
    path('getFlashcardSchemas', views.get_flashcard_schemas, name='get_flashcard_schemas'),
    path('getDbSchemas', views.get_db_schemas, name='get_db_schemas'),
]