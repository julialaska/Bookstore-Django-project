from rest_framework import serializers
from .models import Order, Book, Category, Client, Delivery, Review, BookHasOrder
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    books = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='category-detail')
    title = serializers.CharField(max_length=45)
    description = serializers.CharField(max_length=45)
    books_amount = serializers.CharField(max_length=45)

    class Meta:
        model = Category
        fields = ['pk', 'url', 'title', 'description', 'books_amount', 'books']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.books_amount = validated_data.get('books_amount', instance.books_amount)
        return instance


class BookSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='title')
    author = serializers.CharField(max_length=45)
    title = serializers.CharField(max_length=45)
    price = serializers.IntegerField
    amount = serializers.CharField(max_length=45)
    description = serializers.CharField(max_length=45)
    page_amount = serializers.CharField(max_length=45)
    owner = serializers.ReadOnlyField(source='owner.username')

    def validate_price(self, price):
        if price <= '0':
            raise serializers.ValidationError("Prices can't be lower or equal to zero", )
        return price

    def validate_pages(self, pages):
        if pages <= 0:
            raise serializers.ValidationError("Pages can't be lower or equal to zero", )
        return pages

    class Meta:
        model = Book
        fields = ['url', 'category', 'author', 'title', 'price', 'amount', 'description', 'page_amount','owner']

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.description = validated_data.get('description', instance.description)
        return instance


class ClientSerializer(serializers.ModelSerializer):
    orders = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='order-detail')
    first_name = serializers.CharField(max_length=45)
    surname = serializers.CharField(max_length=45)
    birthdate = serializers.DateField()
    address = serializers.CharField(max_length=45)
    phone_number = serializers.CharField(max_length=9)
    bank_account = serializers.CharField(max_length=45)
    email = serializers.CharField(max_length=45)
    password = serializers.CharField(max_length=45)

    def validate_phone_number(self, value):
        if value != '9':
            raise serializers.ValidationError("Phone number have to consist of 9 digits", )
        return value

    class Meta:
        model = Client
        fields = ['url', 'pk', 'first_name', 'surname', 'birthdate', 'address', 'phone_number',
                  'bank_account', 'email', 'password', 'orders']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.bank_account = validated_data.get('bank_account', instance.bank_account)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        return instance


class DeliverySerializer(serializers.ModelSerializer):
    # orders = serializers.SlugRelatedField(queryset=Order.objects.all(), slug_field='orders')
    price = serializers.CharField(max_length=45)
    type = serializers.CharField(max_length=45)
    time = serializers.CharField(max_length=45)
    priority = serializers.ChoiceField(choices=Delivery.PRIORITY_CHOICES)

    def validate_price(self, price):
        if int(price) <= 0:
            raise serializers.ValidationError("Prices can't be lower or equal to zero", )
        return price

    class Meta:
        model = Delivery
        fields = ['url', 'pk', 'price', 'type', 'time', 'priority']

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.type = validated_data.get('type', instance.type)
        instance.time = validated_data.get('time', instance.time)
        instance.priority = validated_data.get('priority', instance.priority)
        return instance


class OrderSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='surname')
    delivery = serializers.SlugRelatedField(queryset=Delivery.objects.all(), slug_field='pk')
    # book = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field='title')
    quantity = serializers.CharField(max_length=45)
    price = serializers.CharField(max_length=45)
    address = serializers.CharField(max_length=45)
    phone = serializers.CharField(max_length=45)
    date = serializers.DateField()
    status = serializers.CharField(max_length=45)

    def validate_price(self, price):
        if price <= '0':
            raise serializers.ValidationError("Prices can't be lower or equal to zero", )
        return price

    def validate_phone_number(self, value):
        if int(value) != 9:
            raise serializers.ValidationError("Phone number have to consist of 9 digits", )
        return value

    class Meta:
        model = Order
        fields = ['url', 'pk', 'client', 'delivery', 'quantity', 'price', 'address', 'phone', 'date', 'status']

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.date = validated_data.get('date', instance.date)
        instance.status = validated_data.get('status', instance.status)
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field='title')
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='surname')
    scale_points = serializers.CharField(max_length=45)
    read_date = serializers.DateField()
    advantages = serializers.CharField(max_length=45)
    disadvantages = serializers.CharField(max_length=45)
    recommend = serializers.BooleanField()
    read_again = serializers.BooleanField()

    class Meta:
        model = Review
        fields = ['url', 'pk', 'book', 'client', 'scale_points', 'read_date', 'advantages', 'disadvantages',
                  'recommend', 'read_again']

    def update(self, instance, validated_data):
        instance.scale_points = validated_data.get('scale_points', instance.scale_points)
        instance.read_date = validated_data.get('read_date', instance.read_date)
        instance.advantages = validated_data.get('advantages', instance.advantages)
        instance.disadvantages = validated_data.get('disadvantages', instance.disadvantages)
        instance.recommend = validated_data.get('recommend', instance.recommend)
        instance.read_again = validated_data.get('read_again', instance.read_again)
        return instance


class BookHasOrderSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field='title')
    order = serializers.SlugRelatedField(queryset=Order.objects.all(), slug_field='price')

    class Meta:
        model = BookHasOrder
        fields = ['book', 'order']

    def update(self, instance, validated_data):
        instance.book = validated_data.get('book', instance.books)
        instance.order = validated_data.get('order', instance.orders)
        return instance


class UserBookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['url', 'title']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    books = UserBookSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'pk', 'username', 'book']
