from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from recipes.models import Ingredient, Recipe, ShoppingCart, Tag
from users.models import Follow
from .permissions import AuthorOrReadOnly
from .serializers import (CustomUserExtendedSerializer, IngredientSerializer,
                          RecipeMinifiedSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, TagSerializer)
from .services import check_favorites, check_shopping_cart, check_subscriptions

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
        check_favorites(user, recipe, request.method)
        if request.method == 'POST':
            user.favorites.add(recipe)
            serializer = RecipeMinifiedSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.favorites.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()
        check_shopping_cart(user, recipe, request.method)
        if request.method == 'POST':
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeMinifiedSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients_in_cart = Ingredient.objects.filter(
            ingredientinrecipe__recipe__shoppingcart__user=user
        )
        total_ingredients = ingredients_in_cart.annotate(
            sum_=Sum('ingredientinrecipe__amount')
        )
        result = 'Перечень ингредиентов для рецептов из списка покупок:\n'
        for i, item in enumerate(total_ingredients, 1):
            line = f'{i}) {item.name} ({item.measurement_unit}): {item.sum_}\n'
            result += line
        # below is needed for Django 2.2; since v3.2 it supports headers=
        response = HttpResponse(result, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="to_buy.txt"'
        return response


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
        check_subscriptions(user, author, request.method)
        Follow.objects.create(user=user, author=author)
        context = {'request': request}
        serializer = CustomUserExtendedSerializer(author, context=context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        author = get_object_or_404(User, pk=user_id)
        user = request.user
        check_subscriptions(user, author, request.method)
        Follow.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
