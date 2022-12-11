from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from recipes.models import Ingredient, Recipe, Tag
from users.models import Follow
from .permissions import AuthorOrReadOnly
from .serializers import (CustomUserExtendedSerializer, IngredientSerializer,
                          RecipeMinifiedSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, TagSerializer)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка тегов и получение информации о теге по id."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка ингредиентов / информации об ингредиенте по id."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


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

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        recipe = self.get_object()
        already_in_favorites = user.favorites.filter(id=pk).exists()
        if request.method == 'POST':
            if already_in_favorites:
                raise ValidationError({'errors:': 'Уже есть в избранном.'})
            user.favorites.add(recipe)
            serializer = RecipeMinifiedSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if not already_in_favorites:
                raise ValidationError({'errors:': 'Не было в избранном.'})
            user.favorites.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionList(generics.ListAPIView):
    """Получение списка пользователей, на которых подписан текущий юзер."""
    serializer_class = CustomUserExtendedSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class Subscription(APIView):
    http_method_names = ['post', 'delete', 'head', 'options']

    def post(self, request, user_id):
        author = get_object_or_404(User, pk=user_id)
        user = request.user
        if author == user:
            err_msg = 'Невозможно подписаться на самого себя.'
            raise ValidationError({'errors': err_msg})
        if Follow.objects.filter(user=user, author=author).exists():
            err_msg = 'Такая подписка уже существует.'
            raise ValidationError({'errors': err_msg})
        Follow.objects.create(user=user, author=author)
        context = {'request': request}
        serializer = CustomUserExtendedSerializer(author, context=context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        author = get_object_or_404(User, pk=user_id)
        user = request.user
        if not Follow.objects.filter(user=user, author=author).exists():
            raise ValidationError({'errors:': 'Такой подписки не существует.'})
        Follow.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
