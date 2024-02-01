from rest_framework import serializers
from restapi.models import Category, Product, Order, Sales, Quantity
from django.contrib.auth.models import User
from django.conf import settings


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='admin-category-detail', format='html')
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=100)
    products = serializers.HyperlinkedRelatedField(
        many=True, view_name='admin-product-detail', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


def positive_int(value):
    if value < 0:
        raise serializers.ValidationError('Not a positive integer')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='product-detail', format='html')
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=100)
    description = serializers.CharField(
        required=False, allow_blank=True, max_length=500)
    price = serializers.IntegerField(
        required=True, validators=[positive_int])
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    image = serializers.ImageField(
        required=False)
    image_min = serializers.ImageField(
        required=False, read_only=True)
    add = serializers.HyperlinkedIdentityField(
        view_name='product-add', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'category',
            'image',
            'image_min',
            'add'
        ]

    def resize_image(self, original_image):
        from PIL import Image
        img = Image.open(original_image)
        original_width, original_height = img.size
        if original_width < 200:
            return original_image
        aspect_ratio = original_height / original_width
        new_height = round(200*aspect_ratio)
        img = img.resize((200, new_height), Image.LANCZOS)
        file_name = original_image.name
        name_split = file_name.split('.')
        img_name = name_split[0] + '_min.' + name_split[1]
        img_path = settings.MEDIA_ROOT / 'images' / f'{img_name}'
        img.save(img_path)
        return f'images/{img_name}'

    def create(self, validated_data):
        resized_image = self.resize_image(validated_data['image'])
        return Product.objects.create(**validated_data, image_min=resized_image)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('category', instance.category)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        instance.image_min = self.resize_image(validated_data['image'])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    orders = serializers.HyperlinkedRelatedField(
        many=True, view_name='order-details', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'orders']

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class ClientSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    first_name = serializers.CharField(
        required=True, allow_blank=True, max_length=50)
    last_name = serializers.CharField(
        required=True, allow_blank=True, max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class QuantitySerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Quantity
        fields = ['product', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='order-details', format='html')
    client = ClientSerializer()
    street = serializers.CharField(
        required=True, allow_blank=True, max_length=100)
    building = serializers.CharField(
        required=True, allow_blank=True, max_length=10)
    flat = serializers.CharField(
        required=True, allow_blank=True, max_length=10)
    quantities = QuantitySerializer(
        many=True, read_only=True)
    cart_confirmed = serializers.ReadOnlyField()
    order_date = serializers.DateTimeField(
        read_only=True)
    payment_date = serializers.DateTimeField(
        read_only=True)
    summary_price = serializers.IntegerField(
        read_only=True, validators=[positive_int])

    class Meta:
        model = Order
        fields = [
            'id',
            'client',
            'street',
            'building',
            'flat',
            'quantities',
            'cart_confirmed',
            'order_date',
            'payment_date',
            'summary_price'
        ]

    def update(self, instance, validated_data):
        instance.street = validated_data.get('street', instance.street)
        instance.building = validated_data.get('building', instance.building)
        instance.flat = validated_data.get('flat', instance.flat)
        instance.client.first_name = validated_data.get('client').get(
            'first_name', instance.client.first_name)
        instance.client.last_name = validated_data.get('client').get(
            'last_name', instance.client.last_name)
        instance.confirm_cart()
        instance.client.save()
        instance.save()
        return instance


class SalesSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='admin-sales-detail', format='html')
    date_from = serializers.DateTimeField()
    date_to = serializers.DateTimeField()
    quantity = serializers.IntegerField(
        validators=[positive_int])

    class Meta:
        model = Sales
        fields = ['id', 'date_from', 'date_to', 'quantity']

    def update(self, instance, validated_data):
        instance.date_from = validated_data.get('date_from', instance.date_from)
        instance.date_to = validated_data.get('date_to', instance.date_to)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance
