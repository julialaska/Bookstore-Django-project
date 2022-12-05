from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    books_amount = models.CharField(max_length=45)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Book(models.Model):
    category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE)
    author = models.CharField(max_length=45)
    title = models.CharField(max_length=45)
    price = models.CharField(max_length=45)
    amount = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    page_amount = models.CharField(max_length=45)
    owner = models.ForeignKey('auth.User', related_name='books', on_delete=models.CASCADE, null=True, blank=True)

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
        return self.first_name + ' ' + self.surname


class Delivery(models.Model):
    price = models.CharField(max_length=45)
    type = models.CharField(max_length=45)
    # priority = models.BooleanField()
    time = models.CharField(max_length=45)
    TRUE = 'T'
    FALSE = 'F'
    PRIORITY_CHOICES = ((TRUE, 'True'), (FALSE, 'False'),)
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default=FALSE)

    class Meta:
        ordering = ('priority',)

    def __str__(self):
        return self.type


class Order(models.Model):
    client = models.ForeignKey(Client, related_name='orders', on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, related_name='orders', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=45)
    price = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    date = models.DateField()
    status = models.CharField(max_length=45)

    class Meta:
        ordering = ('client',)

    def __str__(self):
        return self.client.surname


class BookHasOrder(models.Model):
    book = models.ForeignKey(Book, related_name='bookhasorders', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='bookhasorders', on_delete=models.CASCADE)


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='reviews', on_delete=models.CASCADE)
    scale_points = models.CharField(max_length=45)
    read_date = models.DateField()
    advantages = models.CharField(max_length=45)
    disadvantages = models.CharField(max_length=45)
    recommend = models.BooleanField()
    read_again = models.BooleanField()
