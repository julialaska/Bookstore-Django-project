from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from . import views
from .models import Category, Client, Book
from rest_framework import status
from django.utils.http import urlencode
from django import urls
from django.contrib.auth.models import User


class CategoryTests(APITestCase):
    def post_category(self, name, description, books_amount):
        url = reverse(views.CategoryList.name)
        data = {'title': name,
                'description': description,
                'books_amount': books_amount}
        response = self.client.post(url, data, format='json')
        return response

    def test_post_and_get_category(self):
        new_category_title = 'IT'
        description = 'technical stuff'
        books_amount = 1000
        response = self.post_category(new_category_title, description, books_amount)
        print("PK {0}".format(Category.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == 1
        assert Category.objects.get().title == new_category_title

    def test_post_existing_category_title(self):
        url = reverse(views.CategoryList.name)
        new_category_title = 'Duplicate IT'
        new_description = "duplicate description"
        new_books_amount = 1234567
        data = {'title': new_category_title,
                'description': new_description,
                'books_amount': new_books_amount}
        response_one = self.post_category(new_category_title, new_description, new_books_amount)
        assert response_one.status_code == status.HTTP_201_CREATED
        response_two = self.post_category(new_category_title, new_description, new_books_amount)
        print(response_one)
        # assert response_two.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_category_by_title(self):
        category_title_one = 'IT'
        category_description_one = "it description"
        category_books_amount_one = 999999
        category_title_two = 'Romance'
        category_description_two = "romance description"
        category_books_amount_two = 5555
        self.post_category(category_title_one, category_description_one, category_books_amount_one)
        self.post_category(category_title_two, category_description_two, category_books_amount_two)
        filter_by_title = {'title': category_title_one}
        url = '{0}?{1}'.format(reverse(views.CategoryList.name), urlencode(filter_by_title))
        print(url)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
        assert response.data['results'][0]['title'] == category_title_one

    def test_get_categories_collection(self):
        new_category_title = 'Anime'
        new_category_description = 'anime desc'
        new_category_books_amount = '89'
        self.post_category(new_category_title, new_category_description, new_category_books_amount)
        url = reverse(views.CategoryList.name)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == new_category_title

    def test_update_category(self):
        category_title = 'IT'
        category_description = 'description'
        category_books_amount = 567
        response = self.post_category(category_title, category_description, category_books_amount)
        url = urls.reverse(views.CategoryDetail.name, None, {response.data['pk']})
        updated_category_title = 'New IT'
        updated_category_description = 'New IT description'
        updated_category_books_amount = '98'
        data = {'title': updated_category_title,
                'description': updated_category_description,
                'books_amount': updated_category_books_amount}
        patch_response = self.client.patch(url, data, format='json')
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['title'] == updated_category_title
        assert patch_response.data['description'] == updated_category_description
        assert patch_response.data['books_amount'] == updated_category_books_amount

    def test_get_category(self):
        category_title = 'IT'
        category_description = 'IT'
        category_books_amount = '66'
        response = self.post_category(category_title, category_description, category_books_amount)
        url = urls.reverse(views.CategoryDetail.name, None, {response.data['pk']})
        get_response = self.client.patch(url, format='json')
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['title'] == category_title
        assert get_response.data['description'] == category_description
        assert get_response.data['books_amount'] == category_books_amount


class BookTests(APITestCase):
    def create_category(self, client):
        url = reverse(views.CategoryList.name)
        data = {'title': 'criminal',
                'description': 'criminal',
                'books_amount': 2}
        client.post(url, data, format='json')

    def post_category(self, name, description, books_amount):
        url = reverse(views.CategoryList.name)
        data = {'title': name,
                'description': description,
                'books_amount': books_amount}
        self.client.post(url, data, format='json')

    def create_book(self, category, author, title, price, amount, description, page_amount, owner, client):
        url = reverse(views.BookList.name)
        data = {'category': category,
                'author': author,
                'title': title,
                'price': price,
                'amount': amount,
                'description': description,
                'page_amount': page_amount,
                'owner': owner}
        response = client.post(url, data, format='json')
        return response

    def test_post_and_get_book(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.login(username='admin', password='admin123')
        self.create_category(client)
        new_category = Category.objects.create(title="Test Category", description="Test Description", books_amount="10")
        new_author = 'Mickiewicz'
        new_title = 'Pan Tadeusz'
        new_price = '45'
        new_amount = '100'
        new_description = 'powiesc'
        new_page_amount = '234'

        response = self.create_book(new_category.title, new_author, new_title, new_price, new_amount, new_description, new_page_amount, user.id, client)
        print(response)
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.count() == 1
        assert Book.objects.get().title == new_title
        assert Book.objects.get().author == new_author

