from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingCartViewSet, FavoriteViewSet,
                    IngredientViewSet, RecipeViewSet, ShoppingCartViewSet,
                    SubscribeViewSet, SubscriptionViewSet, TagsViewSet,
                    UserViewSet)

app_name = 'api'

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'users/(?P<user_id>\d+)/subscribe',
                SubscribeViewSet, basename='to_subscribe')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                FavoriteViewSet, basename='favorites')
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                ShoppingCartViewSet, basename='shopping_cart')


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/subscriptions/', SubscriptionViewSet.as_view({'get': 'list'})),
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCartViewSet.as_view(), name='download'),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
