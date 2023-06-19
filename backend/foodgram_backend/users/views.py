from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework import generics, viewsets, views, mixins, status

from .pagination import MyPagination
from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class AccountViewSet(UserViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = MyPagination

    @action(
            methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated],
            url_path='subscriptions',
            url_name='subscriptions',
            )
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        pages = self.paginate_queryset(
            User.objects.filter(following__user=user)
        )
        serializer = FollowSerializer(
            pages, many=True, context={'user': user, 'request': request})
        return self.get_paginated_response(serializer.data)
