from rest_framework.serializers import ValidationError

from recipes.models import ShoppingCart
from users.models import Follow


def check_favorites(user, recipe, method):
    """Проверка наличие рецепта в избранном."""
    already_in_favorites = user.favorites.filter(id=recipe.id).exists()

    if method == 'POST' and already_in_favorites:
        err_msg = 'Такой рецепт уже есть в избранном.'
        raise ValidationError({'errors:': err_msg})

    if method == 'DELETE' and not already_in_favorites:
        err_msg = 'Такого рецепта не было в избранном.'
        raise ValidationError({'errors:': err_msg})


def check_shopping_cart(user, recipe, method):
    """Проверка наличия рецепта в корзине."""
    already_in_cart = ShoppingCart.objects.filter(user=user, recipe=recipe)

    if method == 'POST' and already_in_cart:
        err_msg = 'Такой рецепт уже есть в списке покупок.'
        raise ValidationError({'errors:': err_msg})

    if method == 'DELETE' and not already_in_cart:
        err_msg = 'Такого рецепта не было в списке покупок.'
        raise ValidationError({'errors:': err_msg})


def check_subscriptions(user, author, method):
    """Проверка наличия подписки и предотвращение подписки на самого себя."""
    is_subscribed = Follow.objects.filter(user=user, author=author).exists()

    if author == user and method == 'POST':
        err_msg = 'Невозможно подписаться на самого себя.'
        raise ValidationError({'errors': err_msg})

    if is_subscribed and method == 'POST':
        err_msg = 'Такая подписка уже существует.'
        raise ValidationError({'errors': err_msg})

    if not is_subscribed and method == 'DELETE':
        err_msg = 'Такой подписки не существует.'
        raise ValidationError({'errors': err_msg})
