from django.db import models
from Authentication.models import User
from Decks.models import Deck, ChineseDeck, JapaneseDeck, KoreanDeck
from . datasets import INDO_EUROPEAN_LANGUAGES
from Decks.datasets import CEFR_LEVELS, HSK_LEVELS, TOPIK_LEVELS, JLPT_LEVELS
from Luabla.models import BaseModel

class FlashcardBase(BaseModel):
    meaning = models.CharField(max_length=200, null=False)
    example_phrase = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(User, related_name="flashcard_author", on_delete=models.CASCADE, db_index=True)
    deck = models.ForeignKey(Deck, related_name="deck", on_delete=models.CASCADE, db_index=True) 

    class Meta:
        abstract = True

class IndoEuropeanFlashcard(FlashcardBase):
    cefr_level = models.CharField(max_length=2, null=False, choices=CEFR_LEVELS, default='A1')
    word = models.CharField(max_length=200, null=True, db_index=True)

    class Meta:
        abstract = True

class Flashcard(IndoEuropeanFlashcard):
    language = models.CharField(max_length=2, choices=INDO_EUROPEAN_LANGUAGES, null=False, db_index=True, default="ES")

    def __str__(self):
        return self.word

class EnglishFlashcard(IndoEuropeanFlashcard):
    author = models.ForeignKey(User, related_name="english_flashcard_author", on_delete=models.CASCADE, db_index=True)
    deck = models.ForeignKey(Deck, related_name="english_deck", on_delete=models.CASCADE, db_index=True)
    language = models.CharField(max_length=2, null=False, default="EN")

    def __str__(self):
        return self.word

class ChineseFlashcard(FlashcardBase):
    hanzi = models.CharField(max_length=40, null=True)
    pinyin = models.CharField(max_length=120, null=True)
    author = models.ForeignKey(User, related_name="chinese_flashcard_author", on_delete=models.CASCADE, db_index=True)
    deck = models.ForeignKey(ChineseDeck, related_name="chinese_deck", on_delete=models.CASCADE, db_index=True) 
    language = models.CharField(max_length=2, null=False, default="ZH")
    hsk_level = models.CharField(max_length=4, null=False, choices=HSK_LEVELS, default='HSK1', db_index=True)

    def __str__(self):
        return self.hanzi
    
class JapaneseFlashcard(FlashcardBase):
    kanji = models.CharField(max_length=50, blank=True, null=True) # Optional (e.g., 食べる)
    kana = models.CharField(max_length=50, null=False) # (e.g., たべる)
    romaji = models.CharField(max_length=100, null=False) # (e.g., "taberu")
    author = models.ForeignKey(User, related_name="japanese_flashcard_author", on_delete=models.CASCADE, db_index=True)
    deck = models.ForeignKey(JapaneseDeck, related_name="japanese_deck", on_delete=models.CASCADE, db_index=True) 
    language = models.CharField(max_length=2, null=False, default="JP")
    jlpt_level = models.CharField(max_length=2, null=False, choices=JLPT_LEVELS, default='N5', db_index=True)

    def __str__(self):
        return self.kana
    
class KoreanFlashcard(FlashcardBase):
    hangul = models.CharField(max_length=50, null=False) # (e.g., "먹다")
    romaji = models.CharField(max_length=100, null=False) # (e.g., "meokda")
    author = models.ForeignKey(User, related_name="korean_flashcard_author", on_delete=models.CASCADE, db_index=True)
    deck = models.ForeignKey(KoreanDeck, related_name="korean_deck", on_delete=models.CASCADE, db_index=True) 
    language = models.CharField(max_length=2, null=False, default="KO")
    topik_level = models.CharField(max_length=10, null=False, choices=TOPIK_LEVELS, default='TOPIK-I-1', db_index=True)

    def __str__(self):
        return self.hangul
    
class RussianFlashcard(FlashcardBase):
    cyrillic = models.CharField(max_length=50, null=False) # (e.g., "говорить")
    transliteration = models.CharField(max_length=100, null=False)
    author = models.ForeignKey(User, related_name="russian_flashcard_author", on_delete=models.CASCADE, db_index=True)
    deck = models.ForeignKey(Deck, related_name="russian_deck", on_delete=models.CASCADE, db_index=True) 
    language = models.CharField(max_length=2, null=False, default="RU")
    cefr_level = models.CharField(max_length=2, null=False, choices=CEFR_LEVELS, default='A1', db_index=True)

    def __str__(self):
        return self.cyrillic

class HindiFlashcard(FlashcardBase):
    devanagari = models.CharField(max_length=50, null=False)  # e.g., "खाना"
    transliteration = models.CharField(max_length=100, null=False)  # e.g., "khānā"
    author = models.ForeignKey(User, related_name="hindi_flashcard_author", on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, related_name="hindi_deck", on_delete=models.CASCADE, db_index=True)
    language = models.CharField(max_length=2, null=False, default="HI")
    cefr_level = models.CharField(max_length=2, null=False, choices=CEFR_LEVELS, default='A1', db_index=True)

    def __str__(self):
        return self.devanagari
