from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ShopIndexView, \
    GroupListView, \
    ProductDetailsView, \
    ProductListView, \
    OrdersListView, \
    OrderDetailView, \
    ProductCreateView, \
    ProductUpdateView, \
    ProductDeleteView, \
    OrderCreateView, \
    OrderUpdateView, \
    OrderDeleteView, \
    ProductsDataExportView, \
    OrdersDataExportView, \
    ProductViewSet, \
    OrderViewSet, LatestProductsFeed

app_name = 'shopapp'

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)

urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path('api/', include(routers.urls)),
    path('groups/', GroupListView.as_view(), name='groups'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/export/', ProductsDataExportView.as_view(), name='products_export'),
    path('products/create/', ProductCreateView.as_view(), name='products_create'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/latest/feed', LatestProductsFeed(), name='products_feed'),
    path('orders/', OrdersListView.as_view(), name='orders'),
    path('orders/export/', OrdersDataExportView.as_view(), name='orders_export'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_details'),
    path('orders/create/', OrderCreateView.as_view(), name='orders_create'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),

]
