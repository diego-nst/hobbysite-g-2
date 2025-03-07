from django.contrib import admin
from .models import Comment, Commission


class CommentInline(admin.TabularInline):
    model = Comment
    list_filter = ('created',)


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    search_fields = ('title',)
    list_display = ('title', 'created',)
    list_filter = ('created',)

    inlines = [CommentInline,]


admin.site.register(Commission, CommissionAdmin)
