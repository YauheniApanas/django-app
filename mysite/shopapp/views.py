from django.contrib.auth.models import User, Group
from django.core import serializers
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from shopapp.models import Product, Order, ProductImage
from .forms import ProductForm, OrderForm, GroupForm


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
