from django.contrib import admin
from .models import JobPosting, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_tier')
    list_filter = ('membership_tier',)
    search_fields = ('user__username', 'user__email')


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'salary_range', 'created_at')
    list_filter = ('location',)
    search_fields = ('title', 'description', 'company_name')
    ordering = ('-created_at',)
