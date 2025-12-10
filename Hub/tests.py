from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from Authentication.models import User
from . models import Post
from rest_framework_simplejwt.tokens import RefreshToken

class PostAPITests(APITestCase):
    def setUp(self):
        # Create user and authenticate
        self.user = User.objects.create_user(username='user1', email='test@example.com', password='testpassword')
        self.client.login(username='user1', password='testpassword')

        # Create test posts
        self.post1 = Post.objects.create(language='EN', title='Post 1', author=self.user, opinion='I think this is the correct way to learn a language: Speaking', speech=None, image=None)
        self.post2 = Post.objects.create(language='ES', title='Post 2', author=self.user, opinion='Pienso que esta es la manera correcta de aprender un lenguaje: Hablar', speech=None, image=None)
        
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies['access_token'] = str(refresh.access_token)
        
    # Tests
    def test_list_posts_by_language(self):
        url = reverse('list_all_posts')

        response = self.client.get(url, {'language': 'EN'})

        print("# Fetched posts by language:", response.data)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['items']), 1)
        
    def test_list_posts_by_user_with_language_filter(self):
        url = reverse('list_posts_by_user')
        
        response = self.client.get(url, {'language': 'EN'})

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('items', response.data)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['language'], 'EN')

    # # Tests for APIView (PostView)
    # def test_post_get(self):
    #     url = reverse('post') + f'?id={self.post1.id}'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, HTTP_200_OK)
    #     self.assertEqual(response.data['item']['title'], self.post1.title)

    # def test_post_put(self):
    #     url = reverse('post') + f'?id={self.post1.id}'
    #     data = {'title': 'Updated', 'opinion': 'Updated content', 'language': 'EN'}
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, HTTP_200_OK)
    #     self.post1.refresh_from_db()
    #     self.assertEqual(self.post1.title, 'Updated')

    # def test_post_patch(self):
    #     url = reverse('post') + f'?id={self.post1.id}'
    #     data = {'title': 'Patched'}
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, HTTP_200_OK)
    #     self.post1.refresh_from_db()
    #     self.assertEqual(self.post1.title, 'Patched')

    # def test_post_delete(self):
    #     url = reverse('post') + f'?id={self.post2.id}'
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
    #     self.assertFalse(Post.objects.filter(id=self.post2.id).exists())


# To include:
# Throttling and permissions in tests.
# Error handling decorators.
# Use fixtures or factory_boy to automatically generate many test posts.

# Execute tests
# python manage.py test myapp