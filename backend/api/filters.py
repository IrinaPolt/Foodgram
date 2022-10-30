from distutils.util import strtobool

import django_filters
from recipes.models import Favorite, Purchase, Recipe
from rest_framework import filters

CHOICES = (
    ('0', 'False'),
    ('1', 'True')
)


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author__id')
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.TypedChoiceFilter(
        choices=CHOICES,
        coerce=strtobool,
        method='get_is_favorited'
    )
    is_in_shopping_cart = django_filters.TypedChoiceFilter(
        choices=CHOICES,
        coerce=strtobool,
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        if not value:
            return queryset
        favorites_pk = Favorite.objects.filter(
            user=self.request.user).values_list('pk', flat=True)
        return queryset.filter(favoriterecipe__in=favorites_pk)

    def get_is_in_shopping_cart(self, queryset, name, value):
        if not value:
            return queryset
        purchases_pk = Purchase.objects.filter(
            user=self.request.user).values_list('pk', flat=True)
        return queryset.filter(recipeincart__in=purchases_pk)


class IngredientFilter(filters.SearchFilter):
    search_param = 'name'
