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
import json
from openai import OpenAI
from django.conf import settings

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_random_flashcards_list(request):
    user = request.user
    language = request.data.get('language')
    requested_flashcards_quantity = request.data.get('quantity') or 20

    if not user.is_authenticated:
        return Response({'error':'Not authorized'}, status=HTTP_401_UNAUTHORIZED)
    
    flashcards_model = {
        'ZH':ChineseFlashcard,
        'JP':JapaneseFlashcard,
        'KO':KoreanFlashcard,
        'RU':RussianFlashcard
    }.get(language, Flashcard)

    flashcard_serializer = {
        'ZH': ChineseFlashcardSerializer,
        'JP': JapaneseFlashcardSerializer,
        'KO': KoreanFlashcardSerializer,
        'RU': RussianFlashcardSerializer
    }.get(language, FlashcardSerializer)

    ids = flashcards_model.objects.values_list('id', flat=True)
    random_ids = random.sample(list(ids), int(requested_flashcards_quantity))
    
    if language == "ZH":
        flashcards = ChineseFlashcard.objects.filter(id__in=random_ids).exclude(hanzi="", meaning="")
    elif language == "JP":
        flashcards = JapaneseFlashcard.objects.filter(id__in=random_ids).exclude(kana="", meaning="")
    elif language == "KO":
        flashcards = KoreanFlashcard.objects.filter(id__in=random_ids).exclude(hangul="", meaning="")
    elif language == "RU":
        flashcards = KoreanFlashcard.objects.filter(id__in=random_ids).exclude(cyrillic="", meaning="")
    else:
        flashcards = Flashcard.objects.filter(id__in=random_ids).exclude(word="", meaning="")

    serialized_flashcards = flashcard_serializer(flashcards, many=True)

    return Response({'flashcards':serialized_flashcards.data}, status=HTTP_200_OK)

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_word_with_ai(request):
    try:
        data = request.data
        language = data.get('language', '').upper()
        native_language = data.get('native_language', '').upper()
        word = data.get('word', '').strip()
        
        # if not language:
        #     error_message = 'Missing language'
        #     return Response({'error': error_message},status=status.HTTP_400_BAD_REQUEST)
        # if not native_language:
        #     error_message = 'Missing native language'
        #     return Response({'error': error_message},status=status.HTTP_400_BAD_REQUEST)
        # if not word:
        #     error_message = 'Missing word'
        #     return Response({'error': error_message},status=status.HTTP_400_BAD_REQUEST)
        
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        language_names = {
            'EN': 'English',
            'ES': 'Spanish',
            'FR': 'French',
            'DE': 'German',
            'IT': 'Italian',
            'PT': 'Portuguese',
            'RU': 'Russian',
            'JP': 'Japanese',
            'KO': 'Korean',
            'ZH': 'Chinese'
        }
        
        target_language_name = language_names.get(language, 'EN')
        native_language_name = language_names.get(native_language, 'ES')
        
        prompt = f"""For the {target_language_name} word/phrase: "{word}"
            Provide:
            1. One concise translation in {native_language_name} (max 3 words)
            2. Three natural example sentences in {target_language_name} (each 5-15 words max)
            Format EXACTLY as JSON:
            {{
                "word_translation": "translation here",
                "sentences": ["sentence1", "sentence2", "sentence3"]
            }}
            Rules:
            - Sentences must use "{word}" naturally
            - Keep sentences simple and practical
            - No explanations, just the JSON
        """

        response = client.chat.completions.create(
            model="gpt-4.1-nano", 
            messages=[
                {"role": "system", "content": "You are a helpful language assistant. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150,  
            n=1
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        if ai_response.startswith('```json'):
            ai_response = ai_response[7:-3].strip()
        elif ai_response.startswith('```'):
            ai_response = ai_response[3:-3].strip()
        
        try:
            parsed_data = json.loads(ai_response)
        except json.JSONDecodeError:
            # If parsing fails, extract JSON manually
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                parsed_data = json.loads(json_match.group())
            else:
                raise ValueError("Invalid JSON response from AI")
        
        if 'word_translation' not in parsed_data or 'sentences' not in parsed_data:
            raise ValueError("Missing required fields in AI response")
        
        sentences = parsed_data['sentences']
        if not isinstance(sentences, list):
            sentences = [sentences]
        
        sentences = [str(s).strip() for s in sentences[:3]]
        
        while len(sentences) < 3:
            sentences.append("")
        
        result = {
            'word_translation': str(parsed_data['word_translation']).strip(),
            'sentences': sentences
        }
        
        return Response({'items': result}, status=status.HTTP_200_OK)
        
    except ValueError as e:
        return Response(
            {'error': f'Processing error: {str(e)}'},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    except Exception as e:
        return Response(
            {'error': f'Internal server error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )