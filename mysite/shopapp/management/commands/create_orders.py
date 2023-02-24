from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Creating order..')
        user = User.objects.get(username='admin')
        products = Product.objects.all()
        order = Order.objects.get_or_create(
            delivery_address='Repina 39',
            promocode='SALE',
            user=user,
        )
        for product in products:
            Order.objects.first().products.add(product)
        Order.objects.first().save()
        self.stdout.write(self.style.SUCCESS(f'Created order {order}'))
