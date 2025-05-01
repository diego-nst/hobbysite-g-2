from django.contrib import admin
from .models import Thread, ThreadCategory, Comment


# class ThreadInline(admin.TabularInline):
#     model = Thread


# class ThreadCategoryAdmin(admin.ModelAdmin):
#     inlines = [ThreadInline,]


# admin.site.register(ThreadCategory, ThreadCategoryAdmin)

class ThreadAdmin(admin.ModelAdmin):
    model = Thread

class ThreadCategoryAdmin(admin.ModelAdmin):
    model = ThreadCategory

class ThreadCommentAdmin(admin.ModelAdmin):
    model = Comment

admin.site.register(Thread, ThreadAdmin)
admin.site.register(ThreadCategory,ThreadCategoryAdmin)
admin.site.register(Comment, ThreadCommentAdmin)

