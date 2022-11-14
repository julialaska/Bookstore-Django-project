from django.http import HttpResponse, Http404
from rest_framework import generics, status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import Book, Category, Client, Order
from .serializers import CategorySerializer, BookSerializer, OrderSerializer, ClientSerializer
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

    # def perform_create(self, serializer):
        # serializer.save(owner=self.request.user)

    # def get(self, request, format=None):
    #     books = Book.objects.all()
    #     serializer = BookSerializer(books, many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request, format=None):
    #     serializer = BookSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    name = 'book-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # def get_object(self, pk):
    #     try:
    #         return Book.objects.get(pk=pk)
    #     except Book.DoesNotExist:
    #         raise Http404
    #
    # def get(self, request, pk, format=None):
    #     book = self.get_object(pk)
    #     serializer = BookSerializer(book)
    #     return Response(serializer.data)
    #
    # def put(self, request, pk, format=None):
    #     book = self.get_object(pk)
    #     serializer = BookSerializer(book, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk, format=None):
    #     book = self.get_object(pk)
    #     book.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
