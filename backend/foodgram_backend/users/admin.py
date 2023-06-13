from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name',)
    list_filter = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')


admin.site.register(User, CustomUserAdmin)
