from django.urls import path
from .views import shop_index, products_list, orders_list, create_products, create_orders

app_name = 'shopapp'
urlpatterns = [
    path('', shop_index, name='index'),
    path('products/', products_list, name='products'),
    path('products/create/', create_products, name='products_create'),
    path('orders/', orders_list, name='orders'),
    path('orders/create/', create_orders, name='orders_create'),
]
