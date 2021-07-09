from django.http import response
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from publishers.models import Publisher

class PublisherTestCase(APITestCase):
    def setUp(self):
        self.host = 'http://localhost:8000'
        self.publisher = Publisher.objects.create(
            name = 'My Publisher',
            founded_year = 2000,
            country = 'british'
        )
        User.objects.create_user(
            username='user', 
            password='password', 
            is_staff=True
        )
        response = self.client.post(
            f'{self.host}/api/token/',
            data={
                'username': 'user', 
                'password': 'password'
            }
        )
        assert response.status_code == 200, response.status_code
        self.token = response.data['access']

        
    def test_get_publishers(self):
        response = self.client.get(
            f'{self.host}/publishers/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.data['results']), 0)


    def test_create_publisher(self):
        data = {
            'name': 'My New Publisher',
            'founded_year': 2021,
            'country': 'Venezuela'
        }
        response = self.client.post(
            f'{self.host}/publishers/', 
            data = data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}', 
            format='json'
        )
        self.assertEqual(response.status_code, 201, response.data)
        total_publishers = Publisher.objects.all().count()
        self.assertNotEqual(total_publishers, 0)


    def test_get_publisher_detail(self):
        response = self.client.get(
            f'{self.host}/publishers/{self.publisher.id}/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}', 
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.publisher.name, response.data['name'])

    
    def test_put_publisher(self):
        data = {
            'name': 'publisher update',
            'founded_year': 2021,
            'country': 'Venezuela'
        }
        response = self.client.put(
            f'{self.host}/publishers/{self.publisher.id}/', 
            data = data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}', 
            format='json'
        )
        self.publisher.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.publisher.name, 'publisher update')


    def test_delete_publisher(self):
        response = self.client.delete(
            f'{self.host}/publishers/{self.publisher.id}/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        total_publishers = Publisher.objects.all().count()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(total_publishers, 0)

    def test_patch_publisher(self):
        data = {
            'name': 'publisher update'
        }
        response = self.client.patch(
            f'{self.host}/publishers/{self.publisher.id}/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}', data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'publisher update')
