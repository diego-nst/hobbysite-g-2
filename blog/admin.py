from django.contrib import admin
from .models import ArticleCategory, Article


class ArticleInline(admin.TabularInline):
    model = Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article)
