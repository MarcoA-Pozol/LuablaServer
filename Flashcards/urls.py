from django.urls import path
from . import views

urlpatterns = [
    path('flashcard', views.FlashcardView.as_view(), name='flashcard'),
    path('randomList', views.get_random_flashcards_list, name='get_random_flashcards_list'),
    path('completeWordWithAI', views.complete_word_with_ai, name='complete_word_with_ai'),
]
