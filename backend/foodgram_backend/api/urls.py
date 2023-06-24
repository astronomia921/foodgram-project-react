from django.urls import include, path

from rest_framework.routers import DefaultRouter

from foodgram.views import RecipeViewSet as RecipeV
from ingredients.views import IngredientViewSet as IngredientV
from tags.views import TagViewSet as TagV
from users.views import AccountViewSet as UserV

app_name = 'api'

api_router_v1 = DefaultRouter()

api_router_v1.register(r'users', UserV, basename='users')
api_router_v1.register(r"tags", TagV, basename="tags")
api_router_v1.register(r"recipes", RecipeV, basename="recipes")
api_router_v1.register(r"ingredients", IngredientV, basename="ingredients")

urlpatterns = [
    path('', include(api_router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
