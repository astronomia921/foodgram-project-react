from django.urls import include, path

from rest_framework.routers import DefaultRouter

from users.views import AccountViewSet
from ingredients.views import IngredientViewSet
from tags.views import TagViewSet

app_name = 'api'

api_router_v1 = DefaultRouter()

api_router_v1.register(r'users', AccountViewSet, basename='users')
api_router_v1.register(r"tags", TagViewSet, basename="tags")
api_router_v1.register(r"ingredients",
                       IngredientViewSet, basename="ingredients")

urlpatterns = [
    path('', include(api_router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
