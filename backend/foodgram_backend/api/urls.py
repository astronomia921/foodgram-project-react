from django.urls import include, path

from rest_framework.routers import DefaultRouter

from users.views import RegistrationViewSet


app_name = 'api'

api_router_v1 = DefaultRouter()

api_router_v1.register(r'users', RegistrationViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(api_router_v1.urls)),
]
