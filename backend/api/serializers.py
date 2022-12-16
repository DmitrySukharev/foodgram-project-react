from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Ingredient, IngredientInRecipe
from recipes.models import Recipe, ShoppingCart, Tag
from users.models import Follow
from .fields import Base64ImageField

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserExtendedSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta():
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes_limit = int(recipes_limit)
        recipe_qs = obj.author_recipes.all()[:recipes_limit]
        serializer = RecipeMinifiedSerializer(
            recipe_qs,
            many=True,
            context={'request': request}
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.author_recipes.count()


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


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.BooleanField()
    is_in_shopping_cart = serializers.BooleanField()
    ingredients = IngredientInRecipeSerializer(
        source='ingredientinrecipe_set',
        many=True
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'text', 'image', 'cooking_time',
                  'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart')


class IngredientInRecipeAddSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')

    def validate_amount(self, value):
        if value < 1:
            err_msg = 'Убедитесь, что количество каждого ингредиента больше 0'
            raise serializers.ValidationError(err_msg)
        return value


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()
    ingredients = IngredientInRecipeAddSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('image', 'name', 'text', 'cooking_time', 'author',
                  'tags', 'ingredients')

    def validate(self, data):
        ingredients = data['ingredients']
        used_ingredients = set([item['id'] for item in ingredients])
        if len(ingredients) > len(used_ingredients):
            err_msg = 'Ингредиенты в рецепте не должны повторяться.'
            raise serializers.ValidationError(err_msg)
        return data

    def validate_cooking_time(self, value):
        if value < 1:
            err_msg = 'Убедитесь, что это значение больше либо равно 1!'
            raise serializers.ValidationError(err_msg)
        return value

    def create_ingredients_in_recipe(self, recipe, ingredients):
        recipe_ingredients_to_create = []
        for ingredient in ingredients:
            new_item = IngredientInRecipe(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
            recipe_ingredients_to_create.append(new_item)
        IngredientInRecipe.objects.bulk_create(recipe_ingredients_to_create)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        current_recipe = Recipe.objects.create(**validated_data)
        current_recipe.tags.add(*tags)
        self.create_ingredients_in_recipe(current_recipe, ingredients)
        return current_recipe

    def update(self, obj, validated_data):
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        for key, value in validated_data.items():
            setattr(obj, key, value)
        if tags:
            obj.tags.clear()
            obj.tags.add(*tags)
        if ingredients:
            obj.ingredients.clear()
            self.create_ingredients_in_recipe(obj, ingredients)
        # save() обязателен - могут быть изменены атрибуты рецепта, напр. имя
        obj.save()
        return obj

    def to_representation(self, obj):
        request = self.context.get('request')
        user = request.user
        cart_qs = ShoppingCart.objects.filter(recipe=obj, user=user)
        obj.is_favorited = obj.user_favorites.filter(id=user.id).exists()
        obj.is_in_shopping_cart = cart_qs.exists()
        serializer = RecipeReadSerializer(obj, context={'request': request})
        return serializer.data
