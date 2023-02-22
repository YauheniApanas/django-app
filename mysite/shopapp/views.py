from django.shortcuts import render


def shop_index(request):
    products = [
        ('apple', 10),
        ('orange', 8),
        ('watermelon', 15),
    ]
    context = {
        'products': products
    }
    return render(request, 'shopapp/shopapp-index.html', context=context)
