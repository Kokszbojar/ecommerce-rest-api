from restapi.models import *
from restapi.serializers import *
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets, mixins


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class SalesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [IsAdminUser]

    def filter_products(self, sales_obj):
        if sales_obj.date_from > sales_obj.date_to:
            return Response("Date to field is smaller than Date from field")
        else:
            orders_queryset = Order.objects.filter(
                order_date__gte=sales_obj.date_from,
                order_date__lte=sales_obj.date_to,
                cart_confirmed=True
            )
            products = {}
            if orders_queryset:
                for order in orders_queryset:
                    product_list = order.product_list.split(',')
                    for product in product_list:
                        try:
                            name = Product.objects.get(id=int(product[0])).name
                        except:
                            continue
                        products[name] = int(product[2])
            sorted_list = sorted(products.items(), key=lambda x:x[1])[::-1]
            if sales_obj.quantity < len(products):
                sorted_list = sorted_list[:sales_obj.quantity]
            products = dict(sorted_list)
            return products

    def retrieve(self, request, pk):
        sales = self.get_object()
        products = self.filter_products(sales)
        return Response(products)
