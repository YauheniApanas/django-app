from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start selecting fields..')
        # product_values = Product.objects.values('pk', 'name')
        # for p_values in product_values:
        #     print(p_values)

        user_info = User.objects.values_list('username', flat=True)
        for user in user_info:
            print(user)
        self.stdout.write(self.style.SUCCESS('Done'))
