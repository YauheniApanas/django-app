from django.shortcuts import render
from django.views.generic import ListView
from .models import Article


class ArticleListView(ListView):
    template_name = 'blogapp/article-list.html'
    queryset = Article.objects.defer('content').select_related('author').select_related('category').prefetch_related('tags').all()
    context_object_name = 'articles'
