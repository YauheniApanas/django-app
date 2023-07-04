from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = 'pk', 'title', 'content', 'pub_date', 'author', 'category'
    # fieldsets = [
    #     (None, {
    #         'fields': ('title', 'content', 'pub_date', 'author', 'category', 'tags')
    #     }),
    # ]

    def get_queryset(self, request):
        return Article.objects.select_related('author').select_related('category').prefetch_related('tags')
