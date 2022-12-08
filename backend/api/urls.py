from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router_1 = DefaultRouter()
router_1.register('ingredients', IngredientViewSet)
router_1.register('tags', TagViewSet)
router_1.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router_1.urls)),
]
