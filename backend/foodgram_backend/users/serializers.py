from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


from .models import Follow

from foodgram.models import Recipe

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_subscribed'
    )
    email = serializers.SerializerMethodField(
        method_name='get_email'
    )
    first_name = serializers.SerializerMethodField(
        method_name='get_first_name'
    )
    last_name = serializers.SerializerMethodField(
        method_name='get_last_name'
    )

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
        }

    def get_subscribed(self, obj):
        """
        Метод проверки наличия подписки у пользователя.
        Если подписан - True, иначе False.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

    def get_email(self, obj):
        if hasattr(obj, 'email'):
            return obj.email
        return None

    def get_first_name(self, obj):
        if hasattr(obj, 'first_name'):
            return obj.first_name
        return None

    def get_last_name(self, obj):
        if hasattr(obj, 'last_name'):
            return obj.last_name
        return None


class UserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                message='Такой email уже занят',
                queryset=User.objects.all()
                )
            ]
        )
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                message='Такой username занят',
                queryset=User.objects.all()
            ),
        ]
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email",
                  "username", "first_name",
                  "last_name", "password")
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
        }


class BaseRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_subscribed'
    )
    recipes = BaseRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = Follow
        fields = (
            'id', 'email',
            'username', 'first_name',
            'last_name', 'is_subscribed',
            'recipes', 'recipes_count',
        )

    def get_subscribed(self, obj):
        """
        Метод проверки наличия подписки у пользователя.
        Если подписан - True, иначе False.
        """
        user = self.context.get("user")
        return Follow.objects.filter(user=user, author=obj).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
