# throttles.py
from rest_framework.throttling import UserRateThrottle

class ListPostsByLanguageThrottle(UserRateThrottle):
    scope = 'list_posts_by_language'
