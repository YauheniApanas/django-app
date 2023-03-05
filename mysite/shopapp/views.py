from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse

from shopapp.models import Product, Order
from .forms import ProductForm, OrderForm


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


def create_products(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('shopapp:products')
            return redirect(url)
    else:
        form = ProductForm()
    context = {
        'form': form,
    }

    return render(request, 'shopapp/create-product.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.prefetch_related('products').select_related('user').all()
    }
    return render(request, 'shopapp/orders-list.html', context=context)


def create_orders(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OrderForm(request.POST)
        user = User.objects.get(username=User.objects.get())
        print(user)
        if form.is_valid():
            address = form.cleaned_data['delivery_address']
            promocode = form.cleaned_data['promocode']
            order = Order.objects.create(delivery_address=address, promocode=promocode, user=request.user)
            for product in form.cleaned_data['products']:
                order.products.add(product)
            url = reverse('shopapp:orders')
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        'form': form,
    }
    return render(request, 'shopapp/orders-create.html', context=context)
