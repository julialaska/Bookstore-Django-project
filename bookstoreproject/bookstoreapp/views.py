from django.http import HttpResponse, Http404
from rest_framework import generics, status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import Book, Category, Client, Order, Delivery, Review, BookHasOrder
from .serializers import CategorySerializer, BookSerializer, \
    OrderSerializer, ClientSerializer, DeliverySerializer, ReviewSerializer, BookHasOrderSerializer
# from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter, FilterSet
from rest_framework import permissions
from django.contrib.auth.models import User


def index(request):
    return HttpResponse("You're at the bookstore.")


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = 'category-list'
    filterset_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['title']


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = 'category-detail'


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    name = 'books'
    filter_fields = ['title', 'category', 'price', 'author']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'category', 'author', 'price']
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    name = 'book-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    name = 'client-list'
    ordering_fields = ['surname', 'birthdate']


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    name = 'client-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    name = 'order-list'


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    name = 'order-detail'


class DeliveryList(generics.ListCreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    name = 'delivery-list'


class DeliveryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    name = 'delivery-detail'


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    name = 'review-list'


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    name = 'review-detail'


class BookHasOrderList(generics.ListCreateAPIView):
    queryset = BookHasOrder.objects.all()
    serializer_class = BookHasOrderSerializer
    name = 'book-has-order-list'


class BookHasOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookHasOrder.objects.all()
    serializer_class = BookHasOrderSerializer
    name = 'book-has-order-detail'
