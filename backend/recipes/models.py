from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

User = get_user_model()

# ToDo: валидатор для формата base64??
# ToDo: Boolean fields - are lowercase true / false in redoc a problem?
# ToDo: Boolean fields - and how about url queries of 0 and 1?


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
        verbose_name = 'тег'

    def __str__(self):
        return self.name[:20]


class Ingredient(models.Model):
    """Ингредиенты рецептов и их единицы измерения."""
    name = models.CharField(
        'Название ингредиента',
        max_length=200,
        unique=True
    )
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta():
        ordering = ('name', )
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name[:50]}, {self.measurement_unit[:10]}'


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
        related_name='author_recipes',
        verbose_name='Автор рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты'
    )

    class Meta():
        verbose_name_plural = 'Рецепты'
        verbose_name = 'рецепт'
        ordering = ('-created_ts', )

    def __str__(self):
        return self.name[:50] + ' by User ' + self.author.username


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
