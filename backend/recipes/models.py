from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.db.models import Exists, OuterRef, Value

User = get_user_model()


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
        max_length=200
    )
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta():
        ordering = ('name', )
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name[:50]}, {self.measurement_unit[:10]}'


class CustomRecipeQueryset(models.QuerySet):
    """Переопредение queryset-а для рецептов и аннотация доп. полями."""
    def with_annotations(self, user):
        if not user.is_authenticated:
            return self.annotate(
                is_favorited=Value(False, models.BooleanField()),
                is_in_shopping_cart=Value(False, models.BooleanField()))

        new_queryset = self.annotate(
            is_favorited=Exists(
                user.favorites.filter(id=OuterRef('pk'))
            ),
            is_in_shopping_cart=Exists(
                ShoppingCart.objects.filter(
                    user=user, recipe__pk=OuterRef('pk'))
            )
        )
        return new_queryset


class Recipe(models.Model):
    """Класс для хранения рецептов."""
    created_ts = models.DateTimeField('Дата публикации', auto_now_add=True)
    name = models.CharField('Название рецепта', max_length=200)
    text = models.TextField('Текст рецепта')
    image = models.ImageField(
        'Картинка к рецепту', upload_to='recipes/images')
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

    objects = CustomRecipeQueryset.as_manager()

    class Meta():
        verbose_name_plural = 'Рецепты'
        verbose_name = 'рецепт'
        ordering = ('-created_ts', )

    def __str__(self):
        return self.name[:50] + ' by User ' + self.author.username


class IngredientInRecipe(models.Model):
    """Ингредиенты, используемые в рецепте, и их количество."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredients')
        ]


class ShoppingCart(models.Model):
    """Рецепты в списке покупок."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_cart_recipes')
        ]
