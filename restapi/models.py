import datetime
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(
        max_length=100, blank=True, default='')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=100, blank=True, default='')
    description = models.CharField(
        max_length=500, blank=True, default='')
    price = models.PositiveIntegerField()
    category = models.ForeignKey(
        'Category', related_name='products', on_delete=models.PROTECT)
    image = models.ImageField(
        upload_to='images', height_field=None, width_field=None, max_length=1440)
    image_min = models.ImageField(
        upload_to='images', height_field=None, width_field=None, max_length=200)

    def __str__(self):
        return f'{self.name} | {self.price}'


class Order(models.Model):
    client = models.ForeignKey(
        User, related_name='orders', on_delete=models.PROTECT)
    street = models.CharField(
        max_length=100, blank=True, default='')
    building = models.CharField(
        max_length=10, blank=True, default='')
    flat = models.CharField(
        max_length=10, blank=True, default='')
    products = models.ManyToManyField(
        'Product', through='Quantity', related_name='orders')
    cart_confirmed = models.BooleanField(
        default=False)
    order_date = models.DateTimeField(
        default=timezone.now)
    payment_date = models.DateTimeField(
        default=timezone.now)
    summary_price = models.PositiveIntegerField(
        default=0)

    class Meta:
        ordering = ['order_date']

    def confirm_cart(self):
        "Calculates dates and applies it to the object fields"
        from datetime import timedelta

        self.cart_confirmed = True
        self.order_date = timezone.now()
        self.payment_date = self.order_date + timedelta(days=5)
        self.save()

    def calculate_price(self):
        self.summary_price = 0
        for product in self.products.all():
            quantity = Quantity.objects.get(order=self, product=product)
            self.summary_price += product.price * quantity.amount
        self.save()

    @receiver(post_save, sender=User)
    def create_handler(sender, instance, **kwargs):
        '''
        Order object is being created after .save() method of User instance.
        Before field "cart_confirmed" becomes True, Order object acts as a cart.
        '''
        if Order.objects.filter(client=instance, cart_confirmed=False):
            pass
        else:
            Order.objects.create(client=instance)

    def __str__(self):
        return f'{self.id} | {self.client.username} | {self.payment_date} | {self.summary_price}'


class Quantity(models.Model):
    order = models.ForeignKey(
        'Order', related_name='quantities', on_delete=models.PROTECT)
    product = models.ForeignKey(
        'Product', on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(
        default=0)

    def __str__(self):
        return f'{self.amount}'


class Sales(models.Model):
    date_from = models.DateTimeField(
        default=datetime.datetime(1924, 1, 22, 11, 42, 5, 2006, tzinfo=datetime.timezone.utc))
    date_to = models.DateTimeField(
        default=datetime.datetime(2124, 1, 22, 11, 42, 5, 2006, tzinfo=datetime.timezone.utc))
    quantity = models.PositiveIntegerField(
        default=100)
