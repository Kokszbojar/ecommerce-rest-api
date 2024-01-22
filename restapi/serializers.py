from rest_framework import serializers
from restapi.models import Category, Product, Order
from django.contrib.auth.models import User
from django.conf import settings

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='category-detail', format='html')
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    products = serializers.HyperlinkedRelatedField(many=True, view_name='product-detail', read_only=True)

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
    id = serializers.HyperlinkedIdentityField(view_name='product-detail', format='html')
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    description = serializers.CharField(required=False, allow_blank=True, max_length=500)
    price = serializers.IntegerField(required=True, validators=[positive_int])
    category = serializers.ReadOnlyField(source='category.name')
    image = serializers.ImageField(required=False)
    image_min = serializers.ImageField(required=False, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'image_min']

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
        img_path = settings.MEDIA_ROOT / 'static' / f'{img_name}'
        img.save(img_path)
        return f'static/{img_name}'

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
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'orders']


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    client = serializers.ReadOnlyField(source='client.username')
    address = serializers.CharField(required=True, allow_blank=True, max_length=200)
    product_list = serializers.DictField(child=serializers.IntegerField(validators=[positive_int]))
    order_date = serializers.DateTimeField(read_only=True)
    payment_date = serializers.DateTimeField(read_only=True)
    summary_price = serializers.IntegerField(read_only=True, validators=[positive_int])

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.product_list = validated_data.get('product_list', instance.product_list)
        instance.save()
        return instance
