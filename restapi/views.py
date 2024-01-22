from restapi.models import Category, Product, Order
from restapi.serializers import CategorySerializer, ProductSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, renderers, viewsets, filters


#class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
#    queryset = Category.objects.all()
#    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name', 'description', 'price']
    ordering_fields = ['name', 'category__name', 'price']

class OrderCreate(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderDetail(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []

        queryset = self.queryset.filter(client=self.request.user)


