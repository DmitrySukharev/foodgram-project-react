from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets

from recipes.models import Ingredient, Recipe, Tag
from .serializers import CustomUserExtendedSerializer
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer

User = get_user_model()


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
    """Получение списка рецептов и доступ к рецепту по id.

    Получение списка рецептов
    Просмотр / добавление / обновление / удаление рецепта по id
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.AllowAny,)


class SubscriptionList(generics.ListAPIView):
    """Получение списка пользователей, на которых подписан текущий юзер."""
    serializer_class = CustomUserExtendedSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
