from rest_framework import serializers
from .models import Order, Book, Category, Client, Delivery, Review


class CategorySerializer(serializers.Serializer):
    books = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='book-category')
    title = serializers.CharField(max_length=45)
    description = serializers.CharField(max_length=45)
    books_amount = serializers.CharField(max_length=45)

    class Meta:
        model = Category
        fields = ['pk', 'url', 'title', 'description', 'books_amount', 'books']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class BookSerializer(serializers.Serializer):
    book_category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    orders = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='order')
    author = serializers.CharField(max_length=45)
    title = serializers.CharField(max_length=45)
    price = serializers.CharField(max_length=45)
    amount = serializers.CharField(max_length=45)
    description = serializers.CharField(max_length=45)
    page_amount = serializers.CharField(max_length=45)

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError("Prices can't be lower or equal to zero", )
        return price

    def validate_pages(self, pages):
        if pages <= 0:
            raise serializers.ValidationError("Pages can't be lower or equal to zero", )
        return pages

    class Meta:
        model = Book
        fields = ['url', 'book_category', 'orders', 'author', 'title', 'price', 'amount', 'description', 'page_amount',
                  'orders']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ClientSerializer(serializers.Serializer):
    book_reviews = serializers.SlugRelatedField(queryset=Review.objects.all(), slug_field='review')
    orders = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='order')
    first_name = serializers.CharField(max_length=45)
    surname = serializers.CharField(max_length=45)
    birthdate = serializers.DateField()
    address = serializers.CharField(max_length=45)
    phone_number = serializers.CharField(max_length=9)
    bank_account = serializers.CharField(max_length=45)
    email = serializers.CharField(max_length=45)
    password = serializers.CharField(max_length=45)

    def validate_phone_number(self, value):
        if value != 9:
            raise serializers.ValidationError("Phone number have to consist of 9 digits", )
        return value

    class Meta:
        model = Client
        fields = ['url', 'pk', 'book_reviews', 'first_name', 'surname', 'birthdate', 'address', 'phone_number',
                  'bank_account', 'email', 'password', 'orders']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class DeliverySerializer(serializers.Serializer):
    orders = serializers.SlugRelatedField(queryset=Order.objects.all(), slug_field='orders')
    price = serializers.CharField(max_length=45)
    type = serializers.CharField(max_length=45)
    time = serializers.CharField(max_length=45)
    priority = serializers.ChoiceField(choices=Delivery.PRIORITY_CHOICES)

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError("Prices can't be lower or equal to zero", )
        return price

    class Meta:
        model = Delivery
        fields = ['url', 'pk', 'price', 'type', 'time', 'priority', 'orders']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class OrderSerializer(serializers.Serializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='client')
    delivery = serializers.SlugRelatedField(queryset=Delivery.objects.all(), slug_field='delivery')
    quantity = serializers.CharField(max_length=45)
    price = serializers.CharField(max_length=45)
    address = serializers.CharField(max_length=45)
    phone = serializers.CharField(max_length=45)
    date = serializers.DateField()
    status = serializers.CharField(max_length=45)

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError("Prices can't be lower or equal to zero", )
        return price

    def validate_phone_number(self, value):
        if value != 9:
            raise serializers.ValidationError("Phone number have to consist of 9 digits", )
        return value

    class Meta:
        model = Delivery
        fields = ['url', 'pk', 'client', 'delivery', 'quantity', 'price', 'address', 'phone', 'date', 'status']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ReviewSerializer(serializers.Serializer):
    books = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field='books')
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='client')
    scale_points = serializers.CharField(max_length=45)
    read_date = serializers.DateField()
    advantages = serializers.CharField(max_length=45)
    disadvantages = serializers.CharField(max_length=45)
    recommend = serializers.BooleanField()
    read_again = serializers.BooleanField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


