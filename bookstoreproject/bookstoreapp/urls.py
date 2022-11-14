from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories', views.CategoryList.as_view(), name=views.CategoryList.name),
    path('categories/<int:pk>', views.CategoryDetail.as_view(), name=views.CategoryDetail.name),
    path('books/', views.BookList.as_view(), name=views.BookList.name),
    path('books/<int:pk>', views.BookDetail.as_view(), name=views.BookDetail.name),
]
