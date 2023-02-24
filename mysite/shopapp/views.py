from django.shortcuts import render
from django.http import HttpRequest

from shopapp.models import Product, Order


def shop_index(request: HttpRequest):
    products = [
        ('apple', 10),
        ('orange', 8),
        ('watermelon', 15),
    ]
    context = {
        'products': products
    }
    return render(request, 'shopapp/shopapp-index.html', context=context)


def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'shopapp/products-list.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.prefetch_related('products').select_related('user').all()
    }
    return render(request, 'shopapp/orders-list.html', context=context)