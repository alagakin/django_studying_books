from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission

from .models import Book, Review


class BookTest(TestCase):

    def setUp(self) -> None:
        self.book = Book.objects.create(
            title='Harry Potter',
            author='JK Rowling',
            price='25.00'
        )
        self.book2 = Book.objects.create(
            title='A day of Ivan Denisovich',
            author='Alexander Solzhenitsyn',
            price='50.00'
        )

        self.special_permission = Permission.objects.get(codename='special_status')

        self.user = get_user_model().objects.create_user(
            username='reviewer',
            email='reviewer@gmail.com',
            password='12345'
        )

        self.review = Review.objects.create(
            author=self.user,
            book=self.book,
            review='An excellent review'
        )

    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'JK Rowling')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view_for_logged_in_users(self):
        self.client.login(email='reviewer@gmail.com', password='12345')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, 'A day of Ivan Denisovich')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_list_view_for_logged_out_users(self):
        self.client.logout()
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/books/' % (reverse('account_login')))
        response = self.client.get('%s?next=/books/' % (reverse('account_login')))
        self.assertContains(response, 'Log In')

    def test_book_detail_view_with_permission(self):
        self.client.login(email='reviewer@gmail.com', password='12345')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, 'An excellent review')
        self.assertTemplateUsed(response, 'books/book_detail.html')


    def test_search_by_author(self):
        self.client.login(email='reviewer@gmail.com', password='12345')
        response = self.client.get(reverse('search_results'), {
            'q': 'JK Rowling'
        })
        self.assertContains(response, 'Harry Potter')
        self.assertNotContains(response, 'A day of Ivan Denisovich')

