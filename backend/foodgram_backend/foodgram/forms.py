from django import forms

from .models import Recipe, Ingredient, Tag


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'author', 'name',
            'image', 'text',
            'ingredients', 'tags',
            'cooking_time',
             ]
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
