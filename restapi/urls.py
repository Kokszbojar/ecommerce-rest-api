from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restapi import views, admin_views

router = DefaultRouter()

# router.register(r'categories',
#                 views.CategoryViewSet,
#                 basename='category')
router.register(r'products',
                views.ProductViewSet,
                basename='product')
router.register(r'orders',
                views.OrderViewSet,
                basename='order')

router.register(r'admin/users',
                admin_views.UserViewSet,
                basename='admin-user')
router.register(r'admin/categories',
                admin_views.CategoryViewSet,
                basename='admin-category')
router.register(r'admin/products',
                admin_views.ProductViewSet,
                basename='admin-product')
router.register(r'admin/orders',
                admin_views.OrderViewSet,
                basename='admin-order')
router.register(r'admin/sales',
                admin_views.SalesViewSet,
                basename='admin-sales')

urlpatterns = [
    path('', include(router.urls)),

    path('products/<int:pk>/add/',
         views.CartAdd.as_view(),
         name='product-add'),
    path('order/<int:pk>/',
         views.OrderDetail.as_view(),
         name='order-details')
]
