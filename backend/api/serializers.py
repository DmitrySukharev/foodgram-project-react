from rest_framework import serializers

from recipes.models import Ingredient, IngredientInRecipe
from recipes.models import Recipe, ShoppingCart, Tag
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source='color_code')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = IngredientInRecipeSerializer(
        source='ingredientinrecipe_set',
        many=True
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'text', 'image', 'cooking_time',
                  'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        return obj.user_favorites.exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        user = request.user
        if not user.is_authenticated:
            return False
        return ShoppingCart.objects.filter(recipe=obj, user=user).exists()
