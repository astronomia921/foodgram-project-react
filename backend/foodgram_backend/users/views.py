from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from djoser.views import UserViewSet

from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .pagination import MyPagination
from .serializers import FollowSerializer

User = get_user_model()


class AccountViewSet(UserViewSet):
    permission_classes = (IsAuthenticated, )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = MyPagination
    search_fields = ['^username', '^email', '^first_name', '^last_name']

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

    @action(
            methods=['post', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_path='subscribe',
            url_name='subscribe',
            )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, id=id)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'POST':
            if user != author:
                Follow.objects.get_or_create(
                    user=user, author=author)
                serializer = FollowSerializer(
                    author,
                    context={
                        'user': user,
                        'author': author,
                        'request': request})
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    )
            else:
                return Response(
                    {'error': 'Вы не можете подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif request.method == 'DELETE':
            Follow.objects.filter(
                user=user, author=author).delete()
            return Response(
                {'message': (
                    f'Подписка на пользователя'
                    f' {user.first_name} {user.last_name} удалена')},
                status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'error': (
                    f'Подписка на пользователя'
                    f' {user.first_name} {user.last_name}не была оформлена.')
                 },
                status=status.HTTP_400_BAD_REQUEST
                )
