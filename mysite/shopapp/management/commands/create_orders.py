from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from shopapp.models import Order, Product


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Creating order..')
        user = User.objects.get(username='admin')
        products = Product.objects.only('id').all()
        order, created = Order.objects.get_or_create(
            delivery_address='Ivanova 39',
            promocode='promo3',
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(self.style.SUCCESS(f'Created order {order}'))
