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
    def post_category(self, title):
        url = reverse(views.CategoryList.title)
        data = {'title': title}
        response = self.client.post(url, data, format='json')
        return response

    def test_post_and_get_category(self):
        new_category_name = 'IT'
        response = self.post_category(new_category_name)
        print("PK {0}".format(Category.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == 1
        assert Category.objects.get().name == new_category_name

    def test_post_existing_category_name(self):
        url = reverse(views.CategoryList.name)
        new_category_name = 'Duplicate IT'
        data = {'name': new_category_name}
        response_one = self.post_category(new_category_name)
        assert response_one.status_code == status.HTTP_201_CREATED
        response_two = self.post_category(new_category_name)
        print(response_two)
        assert response_two.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_category_by_name(self):
        category_name_one = 'IT'
        category_name_two = 'Romance'
        self.post_category(category_name_one)
        self.post_category(category_name_two)
        filter_by_name = {'name': category_name_one}
        url = '{0}?{1}'.format(reverse(views.CategoryList.name), urlencode(filter_by_name))
        print(url)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == category_name_one
