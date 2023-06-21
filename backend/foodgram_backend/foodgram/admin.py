from django.contrib import admin

from .models import (Recipe, RecipeTags,
                     RecipeIngredient, Favorite,
                     ShoppingCart)


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

    def get_tag(sel, obj):
        return ', '.join(
            [str(field) for field in obj.tags.all()]
            )

    get_ingredient.short_description = 'Ингредиенты'
    get_tag.short_description = 'Теги'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('recipe',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('recipe',)


@admin.register(RecipeTags)
class RecipeTagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'tag')
    list_filter = ('recipe', 'tag')
    search_fields = ('recipe', 'tag')
    ordering = ('recipe',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient',)
    search_fields = ('recipe', 'ingredient',)
    ordering = ('recipe',)
