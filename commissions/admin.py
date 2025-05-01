from django.contrib import admin
from .models import JobApplication, Job, Commission


class JobApplicationInline(admin.TabularInline):
    model = JobApplication


class JobInline(admin.TabularInline):
    model = Job
    inlines = [JobApplicationInline,]


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    search_fields = ('title',)
    list_display = ('title', 'created',)
    list_filter = ('created',)

    inlines = [JobInline,]


class JobAdmin(admin.ModelAdmin):
    model = Job
    search_fields = ('role',)
    inlines = [JobApplicationInline,]


class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication
    search_fields = ('role',)


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
