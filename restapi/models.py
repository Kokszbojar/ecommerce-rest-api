from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=500, blank=True, default='')
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static', height_field=None, width_field=None, max_length=1440)
    image_min = models.ImageField(upload_to='static', height_field=None, width_field=None, max_length=200)

    def __str__(self):
        return f'{self.name} | {self.price}'

class Order(models.Model):
    client = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True, default='')
    product_list = models.CharField(max_length=1000, default='error')
    order_date = models.DateTimeField(blank=True, default='cart_not_confirmed')
    payment_date = models.DateTimeField(blank=True, default='cart_not_confirmed')
    summary_price = models.PositiveIntegerField()

    class Meta:
        ordering = ['order_date']

    def confirm_cart(self):
        "Calculates dates and applies it to the object fields"
        from django.utils import timezone
        from datetime import timedelta

        self.order_date = timezone.now()
        self.payment_date = self.order_date + timedelta(days=5)
        super().save()

    def calculate_price(self):
        '''
        Product list string format - "product_id: amount, etc..."
        Below lines format above format to retrieve right prices and sum them for final order price
        '''
        self.summary_price = 0
        products_string_list = self.product_list.split(',').strip()
        products_objects_list = []
        for product in products_string_list:
            product_id = Product.objects.get(id=int(product.split(':')[0]))
            self.summary_price += product.price * int(product.split(':')[1])
        self.save()

    def __str__(self):
        return f'{self.id} | {self.client.username} | {self.payment_date} | {self.summary_price}'

