from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from books.models import Book
from authors.models import Author
from publishers.models import Publisher

class BookTestCase(APITestCase):

    def setUp(self):
        self.host = 'http://localhost:8000'
        self.author = Author.objects.create(
            firstname = 'author',
            lastname = 'author',
            dob = '2000-01-01',
            dod = '2000-01-01',
            nationality = 'Colombian'
        )
        self.publisher = Publisher.objects.create(
            name = 'my_publisher',
            founded_year = 2000,
            country = 'Colombian'
        )
        book = Book.objects.create(
            name='My Book',
            pages=0,
            genre="My genre",
            relased_date='2000-01-01',
            publisher=self.publisher
        )
        book.authors.set([self.author])
        self.book = book
        self.book_id = book.id
        User.objects.create_user(username='user', password='password', is_staff=True)
        response = self.client.post(f'{self.host}/api/token/',
            data={'username': 'user', 'password': 'password'})
        assert response.status_code == 200, response.status_code
        self.token = response.data['access']

    def test_get_books(self):
        response = self.client.get(f'{self.host}/books/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.data['results']), 0)

    def test_create_book(self):
        data = {
            'name': 'book',
            'pages': 0,
            'genre': 'my genre',
            'relased_date': '2000-01-01',
            'authors': [self.author.id],
            'publisher': self.publisher.id
        }
        response = self.client.post(f'{self.host}/books/', data = data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}', format='json')
        self.assertEqual(response.status_code, 201, response.data)
        total_books = Book.objects.all().count()
        self.assertNotEqual(total_books, 0)


    def test_get_book_detail(self):
        response = self.client.get(
            f'{self.host}/books/{self.book.id}/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.book.name, response.data['name'])


    def test_put_book(self):
        data = {
            'name': 'book update',
            'pages': 0,
            'genre': 'my genre',
            'relased_date': '2000-01-01',
            'authors': [self.author.id],
            'publisher': self.publisher.id
        }
        response = self.client.put(
            f'{self.host}/books/{self.book.id}/', 
            data = data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}', 
            format='json'
        )
        self.book.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.book.name, 'book update')


    def test_delete_book(self):
        response = self.client.delete(f'{self.host}/books/{self.book_id}/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}')
        total_books = Book.objects.all().count()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(total_books, 0)


    def test_patch_book(self):
        data = {
            'name': 'book update'
        }
        response = self.client.patch(f'{self.host}/books/{self.book_id}/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'book update')


    def test_get_book_authors(self):
        response = self.client.get(
            f'{self.host}/books/{self.book_id}/authors/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], str(self.author.id))

    
    def test_post_book_authors(self):
        author = Author.objects.create(
            firstname = 'author',
            lastname = 'author',
            dob = '2000-01-01',
            dod = '2000-01-01',
            nationality = 'Colombian'
        )
        data = {
            'authors': [author.id]
        }
        response = self.client.post(f'{self.host}/books/{self.book_id}/authors/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}', data=data, format='json')
        self.book.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.book.authors.all()[0], author)


    def test_delete_book_authors(self):
        response = self.client.delete(
            f'{self.host}/books/{self.book_id}/authors/',
            data = {'authors': [self.author.id]},
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
            format='json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(self.book.authors.all()), 0)


    def test_get_book_publishers(self):
        response = self.client.get(
            f'{self.host}/books/{self.book_id}/publisher/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], str(self.publisher.id))


    def test_post_book_publishers(self):
        publisher = Publisher.objects.create(
            name = 'my_publisher',
            founded_year = 2000,
            country = 'Colombian'
        )
        response = self.client.post(
            f'{self.host}/books/{self.book_id}/publisher/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}', 
            data={'publisher': publisher.id}, 
            format='json'
        )
        self.book.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.book.publisher, publisher)

    def test_delete_book_publisher(self):
        response = self.client.delete(
            f'{self.host}/books/{self.book_id}/publisher/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}', 
        )
        self.book.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.book.publisher, None)