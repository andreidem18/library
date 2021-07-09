from django.http import response
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from authors.models import Author
from books.models import Book
from publishers.models import Publisher

class AuthorTestCase(APITestCase):
    def setUp(self):
        self.host = 'http://localhost:8000'
        self.author = Author.objects.create(
            firstname = 'author_firstname',
            lastname = 'author_lastname',
            dob = '2000-01-01',
            dod = None,
            nationality = 'British'
        )
        User.objects.create_user(
            username='user', 
            password='password', 
            is_staff=True
        )
        response = self.client.post(f'{self.host}/api/token/',
            data={'username': 'user', 'password': 'password'})
        assert response.status_code == 200, response.status_code
        self.token = response.data['access']
        

    def test_get_authors(self):
        response = self.client.get(
            f'{self.host}/authors/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.data['results']), 0)


    def test_create_author(self):
        data = {
            'firstname': 'author_firstname',
            'lastname': 'author_lastname',
            'dob': '2000-01-01',
            'dod': None,
            'nationality': 'British'
        }
        response = self.client.post(
            f'{self.host}/authors/', 
            data = data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}', 
            format='json'
        )
        self.assertEqual(response.status_code, 201, response.data)
        total_authors = Author.objects.all().count()
        self.assertNotEqual(total_authors, 0)

    def test_get_author_detail(self):
        response = self.client.get(
            f'{self.host}/authors/{self.author.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['firstname'], self.author.firstname)


    def test_put_author(self):
        data = {
            'firstname': 'author_firstname update',
            'lastname': 'author_lastname update',
            'dob': '2000-01-01',
            'dod': None,
            'nationality': 'British'
        }
        response = self.client.put(
            f'{self.host}/authors/{self.author.id}/', 
            data = data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}', 
            format='json'
        )
        self.author.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.author.firstname, 'author_firstname update')


    def test_delete_author(self):
        response = self.client.delete(
            f'{self.host}/authors/{self.author.id}/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        total_authors = Author.objects.all().count()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(total_authors, 0)

    def test_patch_author(self):
        data = {
            'firstname': 'author update'
        }
        response = self.client.patch(
            f'{self.host}/authors/{self.author.id}/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}', data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['firstname'], 'author update')

    
    def test_get_author_books(self):
        publisher = Publisher.objects.create(
            name = 'my_publisher',
            founded_year = 2000,
            country = 'Colombian'
        )
        book = Book.objects.create(
            name='My Book',
            pages=0,
            genre="My genre",
            relased_date='2000-01-01',
            publisher=publisher
        )
        book.authors.set([self.author])
        response = self.client.get(
            f'{self.host}/authors/{self.author.id}/books/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
        )
        self.author.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.author.books.all()[0].id, book.id)


    def test_post_author_books(self):
        publisher = Publisher.objects.create(
            name = 'my_publisher',
            founded_year = 2000,
            country = 'Colombian'
        )
        book = Book.objects.create(
            name='My Book',
            pages=0,
            genre="My genre",
            relased_date='2000-01-01',
            publisher=publisher
        )
        response = self.client.post(
            f'{self.host}/authors/{self.author.id}/books/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            data = {'books': [book.id]},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.author.books.all()[0].id, book.id)

    def test_delete_author_books(self):
        publisher = Publisher.objects.create(
            name = 'my_publisher',
            founded_year = 2000,
            country = 'Colombian'
        )
        book = Book.objects.create(
            name='My Book',
            pages=0,
            genre="My genre",
            relased_date='2000-01-01',
            publisher=publisher
        )
        book.authors.set([self.author])
        response = self.client.delete(
            f'{self.host}/authors/{self.author.id}/books/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            data = {'books': [book.id]},
            format = 'json'
        )
        self.author.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(self.author.books.all()), 0)