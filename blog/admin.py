from django.contrib import admin
from .models import ArticleCategory, Article, Comment, ArticleImage


class ArticleInline(admin.TabularInline):
    model = Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]


class CommentInline(admin.TabularInline):
    model = Comment

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage

class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ArticleImageInline]



admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(ArticleImage)
