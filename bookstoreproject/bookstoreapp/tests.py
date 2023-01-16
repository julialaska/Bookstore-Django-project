from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from . import views
from .models import Category, Client, Book, Delivery, Order, BookHasOrder, Review
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
        new_category = Category.objects.create(title="Fantasy", description="fantastic", books_amount="10")
        new_author = 'Mickiewicz'
        new_title = 'Pan Tadeusz'
        new_price = '45'
        new_amount = '100'
        new_description = 'powiesc'
        new_page_amount = '234'

        response = self.create_book(new_category.title, new_author, new_title, new_price, new_amount, new_description,
                                    new_page_amount, user.id, client)
        # print(response)
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.count() == 1
        assert Book.objects.get().title == new_title
        assert Book.objects.get().author == new_author
        assert Book.objects.get().amount == new_amount


class ClientTests(APITestCase):
    def create_client(self, first_name, surname, birthdate, address, phone_number, bank_account, email, password,
                      client):
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
        User.objects.create_superuser('new_admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.login(username='new_admin', password='admin123')
        new_first_name = 'Marek'
        new_surname = 'Nowak'
        new_birthdate = '1974-07-07'
        new_address = 'Polna 20'
        new_phone_number = '987654321'
        new_bank_account = '1222222222'
        new_email = 'nowak@marek.pl'
        new_password = 'mnowak77'
        Client.objects.create(
            first_name=new_first_name,
            surname=new_surname,
            birthdate=new_birthdate,
            address=new_address,
            phone_number=new_phone_number,
            bank_account=new_bank_account,
            email=new_email,
            password=new_password
        )

        assert Client.objects.count() == 1
        assert Client.objects.get().first_name == new_first_name
        assert Client.objects.get().surname == new_surname
        assert Client.objects.get().address == new_address
        assert Client.objects.get().phone_number == new_phone_number


class DeliveryTests(APITestCase):
    def create_delivery(self, price, type, time, priority, client):
        url = reverse(views.DeliveryList.name)
        data = {'price': price,
                'type': type,
                'time': time,
                'priority': priority}
        response = client.post(url, data, format='json')
        return response

    def test_post_and_get_delivery(self):
        User.objects.create_superuser('new_admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.login(username='new_admin', password='admin123')
        new_price = '20'
        new_type = 'poczta polska'
        new_time = '36h'
        new_priority = 'T'
        response = self.create_delivery(new_price, new_type, new_time, new_priority, client)
        print(response)
        assert response.status_code == status.HTTP_201_CREATED
        assert Delivery.objects.count() == 1
        assert Delivery.objects.get().price == new_price
        assert Delivery.objects.get().type == new_type
        assert Delivery.objects.get().time == new_time
        assert Delivery.objects.get().priority == new_priority


class OrderTests(APITestCase):
    def create_client(self):
        client = Client.objects.create(
            first_name='Agata',
            surname='Mazur',
            birthdate='2000-07-23',
            address='Mleczna 56',
            phone_number='777999888',
            bank_account='782378634288934',
            email='mazur@ag.pl',
            password='mazuraga'
        )
        return client

    def create_delivery(self):
        delivery = Delivery.objects.create(
            price='50',
            type='kurier',
            time='2-3 dni',
            priority='F'
        )
        return delivery

    def create_order(self, client, delivery, quantity, price, address, phone, date, status, client_api):
        url = reverse(views.OrderList.name)
        data = {'client': client,
                'delivery': delivery.id,
                'quantity': quantity,
                'price': price,
                'address': address,
                'phone': phone,
                'date': date,
                'status': status
                }
        response = client_api.post(url, data, format='json')
        return response

    def test_post_and_get_order(self):
        client = self.create_client()
        delivery = self.create_delivery()
        client_api = APIClient()
        new_quantity = '2'
        new_price = '50'
        new_address = 'Bursztynowa 78'
        new_phone = '776554332'
        new_date = '2022-01-01'
        new_status = 'w realizacji'
        response = self.create_order(client.surname, delivery, new_quantity, new_price, new_address, new_phone, new_date,
                                     new_status, client_api)

        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1
        assert Order.objects.get().quantity == new_quantity
        assert Order.objects.get().price == new_price
        assert Order.objects.get().address == new_address
        assert Order.objects.get().phone == new_phone


class ReviewTests(APITestCase):
    def create_category(self, client):
        url = reverse(views.CategoryList.name)
        data = {'title': 'criminal',
                'description': 'criminal',
                'books_amount': 2}
        client.post(url, data, format='json')

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
        client.post(url, data, format='json')

    def create_client(self):
        client = Client.objects.create(
            first_name='Agata',
            surname='Mazur',
            birthdate='2000-07-23',
            address='Mleczna 56',
            phone_number='777999888',
            bank_account='782378634288934',
            email='mazur@ag.pl',
            password='mazuraga'
        )
        return client

    def create_review(self, book, client, scale_points, read_date, advantages, disadvantages, recommend, read_again, client_api):
        url = reverse(views.ReviewList.name)
        data = {'book': book,
                'client': client,
                'scale_points': scale_points,
                'read_date': read_date,
                'advantages': advantages,
                'disadvantages': disadvantages,
                'recommend': recommend,
                'read_again': read_again,
                }
        response = client_api.post(url, data, format='json')
        return response

    def test_post_and_get_review(self):
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.login(username='admin', password='admin123')
        self.create_category(client)
        new_category = Category.objects.create(title="Fantasy", description="fantastic", books_amount="10")
        new_book = Book.objects.create(category=new_category, author='tolkien', title='lotr', price='34', amount='2', description='sdas', page_amount='23423', owner=user)
        new_client = self.create_client()
        new_scale_points = '10'
        new_read_date = '2010-10-10'
        new_advantages = 'fun'
        new_disadvantages = 'long'
        new_recommend = True
        new_read_again = True

        response = self.create_review(new_book.title, new_client.surname, new_scale_points, new_read_date, new_advantages, new_disadvantages, new_recommend, new_read_again, client)

        print(response)
        assert response.status_code == status.HTTP_201_CREATED
        assert Review.objects.count() == 1
        assert Review.objects.get().scale_points == new_scale_points
        assert Review.objects.get().advantages == new_advantages

