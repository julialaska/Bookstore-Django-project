from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories', views.CategoryList.as_view(), name=views.CategoryList.name),
    path('categories/<int:pk>', views.CategoryDetail.as_view(), name=views.CategoryDetail.name),
    path('books/', views.BookList.as_view(), name=views.BookList.name),
    path('books/<int:pk>', views.BookDetail.as_view(), name=views.BookDetail.name),
    path('clients', views.ClientList.as_view(), name=views.ClientList.name),
    path('clients/<int:pk>', views.ClientDetail.as_view(), name=views.ClientDetail.name),
    path('orders', views.OrderList.as_view(), name=views.OrderList.name),
    path('orders/<int:pk>', views.OrderDetail.as_view(), name=views.OrderDetail.name),
    path('delivery', views.DeliveryList.as_view(), name=views.DeliveryList.name),
    path('delivery/<int:pk>', views.DeliveryDetail.as_view(), name=views.DeliveryDetail.name),
    path('review', views.ReviewList.as_view(), name=views.ReviewList.name),
    path('review/<int:pk>', views.ReviewDetail.as_view(), name=views.ReviewDetail.name),
    path('book_has_order', views.BookHasOrderList.as_view(), name=views.BookHasOrderList.name),
    path('book_has_order/<int:pk>', views.BookHasOrderDetail.as_view(), name=views.BookHasOrderDetail.name),
]
