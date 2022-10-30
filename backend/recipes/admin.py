from django.contrib import admin
from django.db.models import Count

from .models import (Favorite, Ingredient, Purchase, Recipe, RecipeIngredient,
                     Tag)


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class FavoriteInLine(admin.TabularInline):
    model = Favorite
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_filter = ['name', ]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'get_favorite_count']
    list_filter = ['tags__name', 'author', 'name']
    search_fields = ['name', 'author__username']
    inlines = [RecipeIngredientInLine, FavoriteInLine]
    ordering = ['-id', ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(favorite_count=Count('favoriterecipe'))

    @staticmethod
    def get_favorite_count(obj):
        return obj.favorite_count


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug']
    search_fields = ['name', ]


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']
    search_fields = ['recipe__name', 'user__username']
    autocomplete_fields = ['user', 'recipe']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']
    search_fields = ['user__username', 'recipe__name']
    autocomplete_fields = ['user', 'recipe']
