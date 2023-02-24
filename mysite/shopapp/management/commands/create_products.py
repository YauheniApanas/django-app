from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Creating products..')
        product_names = [
            'laptop',
            'desktop',
            'smartphone',
        ]

        for product_name in product_names:
            product, created = Product.objects.get_or_create(name=product_name)
            if created:
                self.stdout.write(f'Product created {product_name}.')
        self.stdout.write(self.style.SUCCESS('Products created.'))
