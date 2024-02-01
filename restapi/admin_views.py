from restapi.models import Category, Product, Order, Sales
from restapi.serializers import (UserSerializer, CategorySerializer,
                                 ProductSerializer, OrderSerializer,
                                 SalesSerializer)
from django.contrib.auth.models import User
from django.db.models import Q, Sum
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


class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class SalesViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [IsAdminUser]

    def filter_products(self, sales_obj):
        if sales_obj.date_from > sales_obj.date_to:
            return Response("Date to field is smaller than Date from field")
        else:
            summary_queryset = Product.objects.annotate(
                amount=Sum('quantity__amount', filter=Q(
                    quantity__order__order_date__gte=sales_obj.date_from,
                    quantity__order__order_date__lte=sales_obj.date_to,
                    quantity__order__cart_confirmed=True
                    )
                )
            ).order_by('-amount')[:sales_obj.quantity]
            return [{'name': product.name, 'amount': product.amount} for product in summary_queryset]

    def retrieve(self, request, pk):
        sales = self.get_object()
        products = self.filter_products(sales)
        return Response(products)
