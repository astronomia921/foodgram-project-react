from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.foodgram.foodgram_views import RecipeViewSet
from api.ingredients.ingredients_views import IngredientViewSet
from api.tags.tags_views import TagViewSet
from api.users.users_views import AccountViewSet

app_name = 'api'

api_router_v1 = DefaultRouter()

api_router_v1.register(r'users',
                       AccountViewSet,
                       basename='users'
                       )
api_router_v1.register(r"tags",
                       TagViewSet,
                       basename="tags"
                       )
api_router_v1.register(r"recipes",
                       RecipeViewSet,
                       basename="recipes"
                       )
api_router_v1.register(r"ingredients",
                       IngredientViewSet,
                       basename="ingredients"
                       )

urlpatterns = [
    path('', include(api_router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/<int:id>/subscribe/',
        AccountViewSet.as_view(
            {
                'post': 'subscribe',
                'delete': 'unsubscribe'
            }
        ), name='subscribe'),
    path(
        'recipes/<int:pk>/shopping_cart/',
        RecipeViewSet.as_view(
            {
                'post': 'add_to_shopping_cart',
                'delete': 'remove_from_shopping_cart'
            }
        ), name='shopping_cart'),
    path(
        'recipes/<int:pk>/favorite/',
        RecipeViewSet.as_view(
            {
                'post': 'add_to_favorite',
                'delete': 'remove_from_favorite'
            }
        ), name='favorite'),
]
