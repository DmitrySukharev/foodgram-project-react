from django.contrib import admin

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    fields = ('name', 'image', 'text', 'cooking_time', 'tags', 'author', 'ingredient_number')
    readonly_fields = ('ingredient_number',)
    list_display = ('name', 'author')
    list_filter = ('name', 'author__username', 'tags')
    search_fields = ('name',)
    inlines = (IngredientInRecipeInline,)

    def ingredient_number(self, obj):
        return obj.ingredients.count()


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
