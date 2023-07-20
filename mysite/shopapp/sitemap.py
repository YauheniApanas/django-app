from django.contrib.sitemaps import Sitemap

from .models import Product


class ShopSiteMap(Sitemap):
    def items(self):
        return Product.objects.fiter(archived=False).order_by('-created_at')

    def lastmod(self, obj: Product):
        return obj.created_at
