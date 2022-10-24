from django.db import models


class Book(models.Model):
    author = models.CharField(max_length=45)
    title = models.CharField(max_length=45)
    price = models.CharField(max_length=45)
    amount = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    page_amount = models.CharField(max_length=45)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Client(models.Model):
    first_name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    birthdate = models.DateField()
    address = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=9)
    bank_account = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)

    class Meta:
        ordering = ('surname',)

    def __str__(self):
        return self.first_name+' '+self.surname


class Delivery(models.Model):
    price = models.CharField(45)
    type = models.CharField(45)
    priority = models.BooleanField()
    time = models.CharField(45)


class Order(models.Model):
    client = models.ForeignKey(Client, related_name='orders', on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, related_name='delivers', on_delete=models.CASCADE)
    quantity = models.CharField(45)
    price = models.CharField(45)
    address = models.CharField(45)
    phone = models.CharField(45)
    date = models.DateField()
    status = models.CharField(45)


class BookHasOrder(models.Model):
    book = models.ForeignKey(Book, related_name='books', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='orders', on_delete=models.CASCADE)

