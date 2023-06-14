from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_filter = ('name', 'slug',)
    search_fields = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('slug',)
