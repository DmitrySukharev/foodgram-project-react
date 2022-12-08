from rest_framework import permissions, viewsets

from recipes.models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer


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
