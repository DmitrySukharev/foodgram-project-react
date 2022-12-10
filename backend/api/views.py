from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets

from recipes.models import Ingredient, Recipe, Tag
from .permissions import AuthorOrReadOnly
from .serializers import (CustomUserExtendedSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          TagSerializer)

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
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    permission_classes = (AuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubscriptionList(generics.ListAPIView):
    """Получение списка пользователей, на которых подписан текущий юзер."""
    serializer_class = CustomUserExtendedSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
