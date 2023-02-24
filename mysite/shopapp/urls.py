from django.urls import path
from .views import shop_index, products_list, orders_list

app_name = 'shopapp'
urlpatterns = [
    path('', shop_index, name='index'),
    path('products/', products_list, name='products'),
    path('orders/', orders_list, name='orders'),
]
