from csv import DictReader
from io import TextIOWrapper

from django.contrib.auth.models import User

from shopapp.models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding,
    )

    reader = DictReader(csv_file)

    products = [
        Product(**row)
        for row in reader
    ]
    Product.objects.bulk_create(products)
    return products


def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding,
    )
    reader = DictReader(csv_file)
    for row in reader:
        user = User.objects.get(pk=int(row['user']))
        print(user)
        order = Order.objects.create(
            delivery_address=row['delivery_address'],
            promocode=row['promocode'],
            user=user,
        )
        products = [int(item) for item in row['products'].split()]
        for product in products:
            order.products.add(Product.objects.get(pk=product))
        order.save()
    return reader
