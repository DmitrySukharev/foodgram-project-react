from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('Адрес электронной почты', unique=True)
    password = models.CharField('Пароль', max_length=150)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        related_name='user_favorites',
        verbose_name='Избранные рецепты'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)
        verbose_name_plural = 'Пользователи'
        verbose_name = 'пользователя'

    def __str__(self):
        return self.username[:50]


class Follow(models.Model):
    """Подписки на авторов - связь между пользователем и автором."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь, который подписывается'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор, на которого подписываются'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_user_author_pair')
        ]

    def __str__(self):
        return f'Author {self.author.username} - User {self.user.username}'
