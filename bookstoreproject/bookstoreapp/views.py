import django_filters
from django.http import HttpResponse, Http404
from rest_framework import generics, status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import Book, Category, Client, Order, Delivery, Review, BookHasOrder
from .serializers import CategorySerializer, BookSerializer, \
    OrderSerializer, ClientSerializer, DeliverySerializer, ReviewSerializer, BookHasOrderSerializer
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter, FilterSet
from rest_framework import permissions
from django.contrib.auth.models import User


def index(request):
    return HttpResponse("You're at the bookstore.")


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = 'category-list'
    filter_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['title']


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = 'category-detail'


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    name = 'book-list'
    filter_fields = ['title', 'category', 'price', 'author']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'category', 'author', 'price']
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    name = 'book-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ClientFilter(django_filters.FilterSet):
    from_birthdate = DateTimeFilter(field_name='birthdate', lookup_expr='gte')
    to_birthdate = DateTimeFilter(field_name='birthdate', lookup_expr='lte')

    class Meta:
        model = Client
        fields = ['from_birthdate', 'to_birthdate', 'surname']


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    name = 'client-list'
    filterset_class = ClientFilter
    ordering_fields = ['surname', 'birthdate']
    search_fields = ['surname']


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    name = 'client-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class OrderFilter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')
    client_name = AllValuesFilter(field_name='client__surname')

    class Meta:
        model = Order
        fields = ['min_price', 'max_price', 'client_name', 'delivery']


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    name = 'order-list'
    ordering_fields = ['client', 'delivery', 'quantity', 'price', 'status']
    filterset_class = OrderFilter
    search_fields = ['client', 'delivery', 'quantity', 'price', 'status']


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


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'categories': reverse(CategoryList.name, request=request),
                         'books': reverse(BookList.name, request=request),
                         'clients': reverse(ClientList.name, request=request),
                         'orders': reverse(OrderList.name, request=request),
                         'deliveries': reverse(DeliveryList.name, request=request),
                         'reviews': reverse(ReviewList.name, request=request),
                         })
