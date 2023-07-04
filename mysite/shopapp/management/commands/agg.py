from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Count, Sum

from shopapp.models import Product, Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start aggregate..')
        # result = Product.objects.filter(name__contains='Smartphone').aggregate(
        #     Avg('price'),
        #     max_price=Max('price'),
        #     count=Count('id'),
        # )
        # print(result)
        orders = Order.objects.annotate(
            total=Sum('products__price', default=0),
            products_count=Count('products')
        )
        for order in orders:
            print(f'Order {order.id} with {order.products_count} products worth {order.total}')
        self.stdout.write(self.style.SUCCESS('Done'))
