from rest_framework import permissions, viewsets

from recipes.models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка тегов и получение информации о теге по id."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка ингредиентов / информации об ингредиенте по id."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Получение списка рецептов;
    просмотр / добавление / обновление / удаление рецепта.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.AllowAny,)
