from django.contrib import admin

from .models import Book, Category, Client, Order, Delivery, Review, BookHasOrder

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Review)
admin.site.register(BookHasOrder)

