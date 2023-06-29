from django.conf import settings
from django.contrib.auth import models as auth_models
from django.db import models

from foodgram_backend.settings import MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME

from .validators import validate_username


class UserManager(auth_models.BaseUserManager):
    """Кастомный UserManager."""
    def create_user(self,
                    first_name: str, last_name: str,
                    username: str, email: str,
                    password: str = None,
                    is_staff: bool = False,
                    is_superuser: bool = False,
                    ):
        if not email:
            raise ValueError('Пользователь должен иметь email')
        if not first_name:
            raise ValueError('Пользователь должен иметь имя')
        if not last_name:
            raise ValueError('Пользователь должен иметь фамилию')
        if not username:
            raise ValueError('Пользователь должен иметь ник-нейм')
        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         first_name: str, last_name: str,
                         username: str, email: str,
                         password: str = None,
                         ):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.save(using=self._db)
        return user


class User(auth_models.AbstractUser):
    """ Кастомный User."""
    username = models.CharField(
        verbose_name='Ник-нейм',
        validators=[validate_username],
        max_length=MAX_LENGTH_USERNAME,
        help_text='Введите имя пользователя',
        unique=True,
        db_index=True,
        blank=False
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=MAX_LENGTH_EMAIL,
        help_text='Введите адрес электронной почты',
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LENGTH_USERNAME,
        help_text='Введите ваше имя',
        blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LENGTH_USERNAME,
        help_text='Введите вашу фамилию',
        blank=False
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return str(self.username)


class Follow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_users',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='different_users',
            ),
        ]

    def __str__(self):
        return (f'{self.user.username} подписался на'
                f'публикации {self.author.username}')
