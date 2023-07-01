from django.contrib import admin

from apps.ingredients.models import Ingredient


@admin.register(Ingredient)
class IngredientModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    ordering = ('name',)
