from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, mixins

from .serializers import CreateUserSerializer

User = get_user_model()


class RegistrationViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
