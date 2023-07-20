"""
В этом модуле лежат различные наборы представлений.

Разные View интернет-магазина: по товарам, заказм и т.д
"""
import logging
from csv import DictWriter

from django.contrib.auth.models import User, Group
from django.contrib.syndication.views import Feed
from django.core import serializers
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import decorators
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from shopapp.models import Product, Order, ProductImage
from .common import save_csv_products, save_csv_orders
from .forms import ProductForm, OrderForm, GroupForm
from .serializers import ProductsSerializer, OrderSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse

log = logging.getLogger(__name__)


@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.
    Полный CRUD для сущностей товара.
    """
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = ['name', 'description']
    ordering_fields = [
        'name',
        'price',
        'discount',
    ]

    @extend_schema(
        summary='Get one product by ID',
        description='Retrieves **product**, return 404 if not found',
        responses={
            404: OpenApiResponse(description='Empty response, product by id not found'),
            200: ProductsSerializer
        })
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @decorators.action(methods=['get'], detail=False)
    def download_csv(self, request: Request):

        response = HttpResponse(content_type='text/csv')
        filename = 'products-export-csv'
        response['Content-Disposition'] = f'attachment; filename = {filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response

    @decorators.action(methods=['post'], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('products').all()
    serializer_class = OrderSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        'delivery_address',
        'promocode',
        'user',
    ]

    ordering_fields = [
        'delivery_address',
        'promocode',
        'user',
    ]

    @decorators.action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'orders-export-csv'
        response['Content-Disposition'] = f'attachment; filename = {filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'delivery_address',
            'promocode',
            'products',
            'user',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for order in queryset:
            writer.writerow({
                field: getattr(order, field)
                for field in fields
            })
        return response

    @decorators.action(methods=['post'], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        orders = save_csv_orders(
            request.FILES['file'].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('apple', 10),
            ('orange', 8),
            ('watermelon', 15),
        ]
        context = {
            'products': products,
            'items': 2,
        }
        log.debug('Products for shop index: %s', products)
        log.info('Rendering shop index')
        return render(request, 'shopapp/shopapp-index.html', context=context)


class GroupListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'product'


class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'


class ProductCreateView(CreateView):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    # permission_required = 'shopapp.add_product'
    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    success_url = reverse_lazy('shopapp:products')


class ProductUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'shopapp.change_product'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object().created_by
    model = Product
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy()
    form_class = ProductForm

    def get_success_url(self):
        return reverse('shopapp:product_details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image
            )
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class LatestProductsFeed(Feed):
    title = 'Products(latest)'
    description = 'Updates on changes in products'
    link = reverse_lazy('shopapp:products')

    def items(self):
        return (
            Product.objects.filter(archived=False)
            .order_by('-created_at')[:5]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.\
        select_related('user').\
        prefetch_related('products')


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    queryset = Order.objects.\
        select_related('user').\
        prefetch_related('products')


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('shopapp:orders')


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy()

    def get_success_url(self):
        return reverse('shopapp:order_details', kwargs={'pk': self.object.pk})


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders')


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': product.price,
                'archived': product.archived,
            }
            for product in products
        ]
        elem = products_data[0]
        name = elem['name']
        print(name, 'name')
        return JsonResponse({'products': products_data})


class OrdersDataExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'products': [item.pk for item in order.products.all()],
                'user': order.user.pk,
            }
            for order in orders
        ]
        print(orders_data)
        return JsonResponse({'orders': orders_data})
