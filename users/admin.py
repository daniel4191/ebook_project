from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'is_email_verified', 'created_at']
    list_filter = ['is_email_verified', 'created_at']
    search_fields = ['email', 'username']
    ordering = ['-created_at']
