from django.contrib import admin
from .models import Thread, ThreadCategory, Comment


class ThreadAdmin(admin.ModelAdmin):
    '''
    Admin for the Thread model
    '''
    model = Thread


class ThreadCategoryAdmin(admin.ModelAdmin):
    '''
    Admin for the ThreadCategory model
    '''
    model = ThreadCategory


class ThreadCommentAdmin(admin.ModelAdmin):
    '''
    Admin for the Comment model
    '''
    model = Comment


admin.site.register(Thread, ThreadAdmin)
admin.site.register(ThreadCategory, ThreadCategoryAdmin)
admin.site.register(Comment, ThreadCommentAdmin)
