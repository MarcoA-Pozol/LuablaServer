from . models import Flashcard, ChineseFlashcard, JapaneseFlashcard, KoreanFlashcard, RussianFlashcard
from rest_framework.serializers import ModelSerializer

class FlashcardSerializer(ModelSerializer):
    class Meta:
        model = Flashcard
        fields = '__all__' 

class ChineseFlashcardSerializer(ModelSerializer):
    class Meta:
        model = ChineseFlashcard
        fields = '__all__' 

class JapaneseFlashcardSerializer(ModelSerializer):
    class Meta:
        model = JapaneseFlashcard
        fields = '__all__' 

class KoreanFlashcardSerializer(ModelSerializer):
    class Meta:
        model = KoreanFlashcard
        fields = '__all__' 

class RussianFlashcardSerializer(ModelSerializer):
    class Meta:
        model = RussianFlashcard
        fields = '__all__' 