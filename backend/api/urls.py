from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet,
                    Subscription, SubscriptionList, TagViewSet)

router_1 = DefaultRouter()
router_1.register('ingredients', IngredientViewSet)
router_1.register('tags', TagViewSet)
router_1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_1.urls)),
    path('users/subscriptions/',
         SubscriptionList.as_view(), name='subscriptions'),
    path('users/<int:user_id>/subscribe/',
         Subscription.as_view(), name='subscribe')
]
