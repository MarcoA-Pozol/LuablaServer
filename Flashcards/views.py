from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from . models import Flashcard, ChineseFlashcard, JapaneseFlashcard, KoreanFlashcard, RussianFlashcard
from Decks.models import Deck, ChineseDeck, JapaneseDeck, KoreanDeck
from . serializers import FlashcardSerializer, ChineseFlashcardSerializer, JapaneseFlashcardSerializer, KoreanFlashcardSerializer, RussianFlashcardSerializer
from rest_framework.decorators import api_view, permission_classes
import random

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_random_flashcards_list(request):
    user = request.user
    language = request.data.get('language')
    requested_flashcards_quantity = request.data.get('quantity')

    if user is not IsAuthenticated:
        return Response({'error':'Not authorized'}, status=HTTP_401_UNAUTHORIZED)
    
    flashcards_model = {
        'ZH':ChineseFlashcard,
        'JP':JapaneseFlashcard,
        'KO':KoreanFlashcard,
        'RU':RussianFlashcard
    }.get(language, Flashcard)

    ids = flashcards_model.objects.values_list('id', flat=True)
    random_ids = random.sample(ids, requested_flashcards_quantity)
    
    flashcards = flashcards_model.objects.filter(id__in=random_ids)
    serialized_flashcards = FlashcardSerializer(flashcards, many=True)

    return Response({'flashcards':serialized_flashcards}, status=HTTP_200_OK)

class FlashcardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):


        try:
            deck_id = request.query_params.get('id')
            language = request.query_params.get('language')

            flashcard_model = {
                'ZH': ChineseFlashcard,
                'JP': JapaneseFlashcard,
                'KO': KoreanFlashcard,
                'RU': RussianFlashcard
            }.get(language, Flashcard)

            flashcard_serializer = {
                'ZH': ChineseFlashcardSerializer,
                'JP': JapaneseFlashcardSerializer,
                'KO': KoreanFlashcardSerializer,
                'RU': RussianFlashcardSerializer
            }.get(language, FlashcardSerializer)

            flashcards_list = flashcard_serializer(flashcard_model.objects.filter(deck=deck_id).all(), many=True)

            return Response({'flashcards':flashcards_list.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':f'Unexpected error: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            deck_id = request.query_params.get('deckId')
            language = request.query_params.get('language')
            word = request.data.get('word')
            hanzi = request.data.get('hanzi')
            pinyin = request.data.get('pinyin')
            kanji = request.data.get('kanji')
            kana = request.data.get('kana')
            romaji = request.data.get('romaji')
            hangul = request.data.get('hangul')
            cyrillic = request.data.get('cyrillic')
            transliteration = request.data.get('transliteration')
            meaning = request.data.get('meaning')
            example_phrase = request.data.get('examplePhrase')
            author = request.user
        except Exception as e:
            response = Response({'error': 'Error obtaining request data'}, status=status.HTTP_400_BAD_REQUEST)
            return response
    
        try:
            if language == 'ZH':
                deck = ChineseDeck.objects.get(id=deck_id)
                flashcard = ChineseFlashcard.objects.create(hanzi=hanzi, pinyin=pinyin, meaning=meaning, example_phrase=example_phrase, author=author, deck=deck)
            elif language == 'JP':
                deck = JapaneseDeck.objects.get(id=deck_id)
                flashcard = JapaneseFlashcard.objects.create(kanji=kanji, kana=kana, romaji=romaji, meaning=meaning, example_phrase=example_phrase, author=author, deck=deck)
            elif language == 'KO':
                deck = KoreanDeck.objects.get(id=deck_id)
                flashcard = KoreanFlashcard.objects.create(hangul=hangul, romaji=romaji, meaning=meaning, example_phrase=example_phrase, author=author, deck=deck)
            elif language == 'RU':
                deck = Deck.objects.get(id=deck_id)
                flashcard = RussianFlashcard.objects.create(cyrillic=cyrillic, transliteration=transliteration, meaning=meaning, example_phrase=example_phrase, author=author, deck=deck)
            else:
                deck = Deck.objects.get(id=deck_id)
                flashcard = Flashcard.objects.create(word=word, meaning=meaning, example_phrase=example_phrase, author=author, deck=deck)

            flashcard.save()

            # Increase cards quantity in deck where flashcard is added
            deck.cards_quantity+=1
            deck.save()

            return Response({'message':'Flashcard was created'}, status=status.HTTP_201_CREATED)
        
        except Deck.DoesNotExist:
            return Response({'error': 'Deck not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e: 
            return Response({'error': f'Error during flashcard creation ({e})'}, status=status.HTTP_400_BAD_REQUEST)
