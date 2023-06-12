from django.contrib import admin

from .models import Recipe, Tag, Ingredient


class RecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


@admin.register(Recipe)
class RecipeModelAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'cooking_time',
                    'get_ingredient', 'get_tag')
    fields = ('author', 'name', 'image',
              'text', 'cooking_time', )
    inlines = [
        RecipeInline, TagInline
    ]
    list_filter = ('name', 'cooking_time',)
    search_fields = ('name', 'text',)
    raw_id_fields = ('author',)
    ordering = ('name',)

    def get_ingredient(self, obj):
        return ', '.join(
            [str(field) for field in obj.ingredients.all()]
            )

    def get_tag(sel, obj):
        return ', '.join(
            [str(field) for field in obj.tags.all()]
            )


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_filter = ('name', 'slug',)
    search_fields = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('slug',)


@admin.register(Ingredient)
class IngredientModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    ordering = ('name',)
