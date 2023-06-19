from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.conf import settings

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers
from django.urls import reverse
from django.test import Client


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='admin')
        user.set_password('zxczxc123')
        user.save()

    def test_create_product(self):
        c = Client()
        c.login(username='admin', password='zxczxc123')
        response = c.post(
            reverse('shopapp:products_create'),
            {
                'name': 'table',
                'price': '123.45',
                'description': 'a good table',
                'discount': '10',
            }
        )
        self.assertRedirects(response, reverse('shopapp:products'))


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        user = User.objects.create(username='admin')
        cls.product = Product.objects.create(name='best product', created_by=user)

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_links(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'product-fixture.json',
        'user-fixture.json',
        'group-fixture.json',
    ]

    def test_products(self):
        response = self.client.get(reverse('shopapp:products'))
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context['products']),
            transform=lambda p: p.pk,
            ordered=False,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test', password='qwerty')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse('shopapp:orders'))
        self.assertContains(response, 'Orders')

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'product-fixture.json',
        'user-fixture.json',
        'group-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test', password='qwerty', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_products_view(self):
        response = self.client.get(reverse('shopapp:products_export'))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': product.price,
                'archived': product.archived,
            }
            for product in products
        ]

        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expected_data,
        )


class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test', password='qwerty')
        cls.user.user_permissions.add(Permission.objects.get(codename='view_order'))
        cls.order = Order.objects.create(delivery_address='Pushkina', promocode='sale', user=cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.order.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_details', kwargs={'pk': self.order.pk}))
        self.assertContains(response, 'Delivery address')
        self.assertContains(response, 'Promocode')
        self.assertContains(response, self.order.pk)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'product-fixture.json',
        'order-fixture.json',
        'user-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test', password='qwerty', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_export_view(self):
        response = self.client.get(reverse('shopapp:orders_export'))
        orders = Order.objects.all()
        expected_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'products': order.products,
                'user': order.user,
            }
            for order in orders
        ]

        orders_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            orders_data['orders'],
            expected_data,
        )
