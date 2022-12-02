from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

User = get_user_model()


# ToDo: ManyToMany Recipes - Ingredients
# ToDo: __str__ for recipes
# ToDo: валидатор для формата base64?
# Boolean fields - are lowercase true / false in redoc a problem?
# Boolean fields - and how about url queries of 0 and 1?
class Tag(models.Model):
    """Теги для рецептов."""
    name = models.CharField('Название тега', max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    color_code = models.CharField(
        'HEX-код цвета',
        unique=True,
        max_length=7,
        validators=[MinLengthValidator(7)]
    )

    class Meta():
        ordering = ('name', )
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:20]


class Ingredient(models.Model):
    """Ингредиенты рецептов и их единицы измерения."""
    name = models.CharField('Название ингредиента', max_length=200)
    uom = models.CharField('Единица измерения', max_length=200)

    class Meta():
        ordering = ('name', )
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name[:50]}, {self.uom[:10]}'


class Recipe(models.Model):
    """Класс для хранения рецептов."""
    created_ts = models.DateTimeField('Дата публикации', auto_now_add=True)
    name = models.CharField('Название рецепта', max_length=200)
    text = models.TextField('Текст рецепта')
    image = models.TextField('Картинка к рецепту (base64)')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах', validators=[MinValueValidator(1)])
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    is_favorited = models.BooleanField('Статус избранного')
    is_in_shopping_cart = models.BooleanField('Статус нахождения в корзине')

    class Meta():
        verbose_name_plural = 'Рецепты'
        ordering = ('-created_ts', )

    def __str__(self):
        return self.name[:50] + 'by User' + self.author
