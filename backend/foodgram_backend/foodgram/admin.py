from django.contrib import admin

from .models import Recipe


class RecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


@admin.register(Recipe)
class RecipeModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'pub_date', 'cooking_time',
                    'get_ingredient', 'get_tag')
    fields = ('author', 'name', 'image',
              'text', 'cooking_time', )
    inlines = [
        RecipeInline, TagInline
    ]
    list_filter = ('name', 'pub_date', 'cooking_time',)
    search_fields = ('name', 'pub_date',)
    ordering = ('-pub_date',)

    def get_ingredient(self, obj):
        return ', '.join(
            [str(field) for field in obj.ingredients.all()]
            )

    get_ingredient.short_description = 'Ингредиенты'

    def get_tag(sel, obj):
        return ', '.join(
            [str(field) for field in obj.tags.all()]
            )

    get_tag.short_description = 'Теги'
