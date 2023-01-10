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
    def post_category(self, name):
        url = reverse(views.CategoryList.name)
        data = {'name': name}
        response = self.client.post(url, data, format='json')
        return response

    def test_post_and_get_category(self):
        new_category_title = 'IT'
        response = self.post_category(new_category_title)
        print("PK {0}".format(Category.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == 1
        assert Category.objects.get().title == new_category_title

    def test_post_existing_category_title(self):
        url = reverse(views.CategoryList.name)
        new_category_title = 'Duplicate IT'
        data = {'title': new_category_title}
        response_one = self.post_category(new_category_title)
        assert response_one.status_code == status.HTTP_201_CREATED
        response_two = self.post_category(new_category_title)
        print(response_two)
        assert response_two.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_category_by_title(self):
        category_title_one = 'IT'
        category_title_two = 'Romance'
        self.post_category(category_title_one)
        self.post_category(category_title_two)
        filter_by_title = {'title': category_title_one}
        url = '{0}?{1}'.format(reverse(views.CategoryList.name), urlencode(filter_by_title))
        print(url)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == category_title_one

    def test_get_categories_collection(self):
        new_category_title = 'Anime'
        self.post_category(new_category_title)
        url = reverse(views.CategoryList.name)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == new_category_title

    def test_update_category(self):
        category_title = 'IT'
        response = self.post_category(category_title)
        url = urls.reverse(views.CategoryDetail.name, None, {response.data['pk']})
        updated_category_title = 'New IT'
        data = {'title': updated_category_title}
        patch_response = self.client.patch(url, data, format='json')
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['title'] == updated_category_title

    def test_get_category(self):
        category_title = 'IT'
        response = self.post_category(category_title)
        url = urls.reverse(views.CategoryDetail.name, None, {response.data['pk']})
        get_response = self.client.patch(url, format='json')
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['title'] == category_title


class ClientTests(APITestCase):
    def create_client(self,  first_name, surname, birthdate, address, phone_number, bank_account, email, password, client):
        url = reverse(views.ClientList.name)
        data = {'first_name': first_name,
                'surname': surname,
                'birthdate': birthdate,
                'address': address,
                'phone_number': phone_number,
                'bank_account': bank_account,
                'email': email,
                'password': password
                }
        response = client.post(url, data, format='json')
        return response

    def test_post_and_get_client(self):
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.login(username='admin', password='admin123')
        new_first_name = 'Marek'
        new_surname = 'Nowak'
        new_birthdate = '1974-08-09'
        new_address = 'Polna 14'
        new_phone_number = 123456789
        new_bank_account = 111111111111111111
        new_email = 'mnowak@nowak.pl'
        new_password = 'nowak123'
        response = self.create_client(new_first_name, new_surname, new_birthdate, new_address, new_phone_number, new_bank_account, new_email, new_password, client)
        assert response.status_code == status.HTTP_201_CREATED
        assert Client.objects.count() == 1
        assert Client.objects.get().first_name == new_first_name
        assert Client.objects.get().last_name == new_surname

