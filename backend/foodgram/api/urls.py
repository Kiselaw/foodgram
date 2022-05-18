from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CartListView, CartViewSet, FavoriteViewSet, FollowsViewSet,
                    FollowViewSet, IngredientViewSet, RecipeViewSet,
                    TagViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)
router.register('users/subscriptions',
                FollowsViewSet, basename='subscriptions')
router.register(r'users/(?P<author_id>\d+)/subscribe',
                FollowViewSet, basename='subscribe')
router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                FavoriteViewSet, basename='favorite')
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                CartViewSet, basename='shopping_cart')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('recipes/download_shopping_cart', CartListView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
]
