from restapi.models import Product, Order, Quantity
from restapi.serializers import ProductSerializer, OrderSerializer
from restapi.permissions import IsOwnerOrAdminOnly

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets, filters

from django.core.mail import send_mail
from django.http import Http404
from django.db import IntegrityError, transaction


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name', 'description', 'price']
    ordering_fields = ['name', 'category__name', 'price']


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOnly]

    def list(self, request):
        serializer_context = {
            'request': request,
        }
        queryset = Order.objects.filter(client=request.user)
        serializer = OrderSerializer(queryset, many=True,
                                     context=serializer_context)
        return Response(serializer.data)


def send_confirmation_email(request, order):
    subject = 'Order - {order.id}'
    message = str('This is a confirmation email.' +
                  'You have successfully placed your order' +
                  'to purchase items from mysite.com')
    from_email = 'noreply@mysite.com'
    recipient_list = [request.user.email]
    send_mail(subject, message, from_email, recipient_list)


class OrderDetail(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOnly]

    def get(self, request, pk):
        return self.retrieve(request)

    @transaction.atomic
    def put(self, request, pk):
        order = Order.objects.get(pk=pk)
        if not order.cart_confirmed and order.products.all():
            send_confirmation_email(request, order)
        else:
            return Response("Action not allowed")
        return self.update(request)


class CartAdd(APIView):
    def get_order(self, request):
        try:
            return Order.objects.get(client=request.user,
                                     cart_confirmed=False)
        except Order.DoesNotExist:
            raise Http404

    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def add_one_to_cart(self, order, product):
        try:
            quantity, created = Quantity.objects.get_or_create(order=order, product=product)
            with transaction.atomic():
                quantity.amount += 1
                quantity.save()
                order.calculate_price()
        except IntegrityError:
            return "Error occured while trying to edit cart"
        return "Added one to cart"

    def get(self, request, pk):
        order = self.get_order(request)
        product = self.get_product(pk)
        return Response(self.add_one_to_cart(order, product))
