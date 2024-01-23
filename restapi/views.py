from restapi.models import Product, Order
from restapi.serializers import ProductSerializer, OrderSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets, filters, status

from django.core.mail import send_mail


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name', 'description', 'price']
    ordering_fields = ['name', 'category__name', 'price']

def send_confirmation_email(request, order):
    subject = 'Order - {order.id}'
    message = 'This is a confirmation email. You have successfully placed your order to purchase items from mysite.com'
    from_email = 'admin@mysite.com'
    recipient_list = [request.user.email]
    send_mail(subject, message, from_email, recipient_list)

class OrderDetail(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        id = request.path.split('/')[2]
        order = Order.objects.get(id=id)
        if order.client == request.user or request.user.is_staff:
            pass
        else:
            queryset = []
        return self.retrieve(request)

    def put(self, request, pk):
        id = request.path.split('/')[2]
        order = Order.objects.get(id=id)
        if (order.client == request.user and not order.cart_confirmed) or request.user.is_staff:
            send_confirmation_email(request, order)
        else:
            queryset = []
        return self.update(request)

class CartAdd(APIView):
    def get_order(self, request):
        try:
            return Order.objects.get(client=request.user, cart_confirmed=False)
        except Order.DoesNotExist:
            raise Http404

    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def add_one_to_cart(self, order, product):
        product_list = order.product_list.split(',')
        order.product_list = ''
        new_id = True
        for item in product_list:
            item_list = item.split(':')
            if item_list[0] == '':
                continue
            elif product.id == int(item_list[0]):
                item = f'{product.id}:{int(item_list[1])+1},'
                new_id = False
            else:
                item += ','
            order.product_list += item
        if order.product_list != '' and new_id == False:
            order.product_list = order.product_list[:-1]
        else:
            order.product_list += f'{product.id}:1'
        order.save()
        return "Added one to cart"

    def remove_one_from_cart(self, order, product):
        product_list = order.product_list.split(',')
        order.product_list = ''
        for item in product_list:
            item_list = item.split(':')
            if product.id == int(item_list[0]) and int(item_list[1]) > 1:
                item = f'{product.id}:{int(item_list[1])-1},'
            elif product.id == int(item_list[0]):
                continue
            else:
                item.join(',')
            order.product_list.join(item)
        if order.product_list != '':
            order.product_list = order.product_list[:-1]
        order.save()
        return "Removed one from cart"

    def get(self, request, pk):
        order = self.get_order(request)
        product = self.get_product(pk)
        return Response(self.add_one_to_cart(order, product))
