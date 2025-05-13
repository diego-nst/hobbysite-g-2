from django.contrib import admin
from .models import ArticleCategory, Article, Comment, ArticleImage


class ArticleInline(admin.TabularInline):
    '''
    Admin in line for Article
    '''
    model = Article


class CommentInLine(admin.TabularInline):
    '''
    Admin in line for Comment
    '''
    model = Comment


class ArticleImageInline(admin.TabularInline):
    '''
    Admin in line for Article Image
    '''
    model = ArticleImage


class ArticleAdmin(admin.ModelAdmin):
    '''
    Admin panel for Article with Comments and ArticleImage as in lines
    '''
    inlines = [CommentInLine,  ArticleImageInline]


class ArticleCategoryAdmin(admin.ModelAdmin):
    '''
    Admin panel for ArticleCategory with Article as in line
    '''
    inlines = [ArticleInline]


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(ArticleImage)
