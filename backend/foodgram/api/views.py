from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter
from .models import (Cart, CustomUser, Favorite, Follow, Ingredient, Recipe,
                     RecipeIngredient, Tag)
from .permissions import IsAuthorOrReadOnly
from .serializers import (CartSerializer, FavoriteSerializer,
                          FollowPostSerializer, FollowsSerializer,
                          IngredientSerializer, RecipePostSerializer,
                          RecipeSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'delete', 'head', 'patch', 'options']
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly
    ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = Recipe.objects.all()
        user = self.request.user
        query_params = self.request.query_params
        is_favorited = query_params.get('is_favorited')
        is_in_shopping_cart = query_params.get('is_in_shopping_cart')
        if user.is_authenticated and is_favorited:
            favorite_recipes_id = (
                user.favorites.all()
            ).values_list('recipe__id', flat=True).distinct()
            queryset = Recipe.objects.filter(id__in=favorite_recipes_id)
            return queryset
        if user.is_authenticated and is_in_shopping_cart:
            in_cart_recipes_id = (
                user.in_cart.all()
            ).values_list('recipe__id', flat=True).distinct()
            queryset = Recipe.objects.filter(id__in=in_cart_recipes_id)
            return queryset
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipePostSerializer
        return RecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    permission_classes = [permissions.AllowAny]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.AllowAny]


class FollowsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FollowsSerializer

    def get_queryset(self):
        user = self.request.user
        followings_user_id = (
            (user.following.all())
            .values_list('author__id', flat=True).distinct()
        )
        subscriptions = CustomUser.objects.filter(id__in=followings_user_id)
        return subscriptions


class FollowViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowPostSerializer

    def get_queryset(self):
        follower = self.request.user
        subscriptions = follower.following.all()
        return subscriptions

    def perform_create(self, serializer):
        author_id = self.kwargs.get("author_id")
        author = CustomUser.objects.get(pk=author_id)
        serializer.save(user=self.request.user, author=author)

    def delete(self, *args, **kwargs):
        author_id = self.kwargs.get("author_id")
        author = CustomUser.objects.get(pk=author_id)
        author_in_subscriptions = Follow.objects.get(
            user=self.request.user, author=author
        )
        author_in_subscriptions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        user = self.request.user
        favorites = user.favorites.all()
        return favorites

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get("recipe_id")
        recipe = Recipe.objects.get(pk=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

    def delete(self, *args, **kwargs):
        recipe_id = self.kwargs.get("recipe_id")
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe_in_favorite = Favorite.objects.get(
            user=self.request.user, recipe=recipe
        )
        recipe_in_favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        cart = user.in_cart.all()
        return cart

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get("recipe_id")
        recipe = Recipe.objects.get(pk=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

    def delete(self, *args, **kwargs):
        recipe_id = self.kwargs.get("recipe_id")
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe_in_cart = Cart.objects.get(
            user=self.request.user, recipe=recipe
        )
        recipe_in_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartListView(APIView):

    def get(self, request):
        user = self.request.user
        recipes_id = (
            user.in_cart.all().values_list('recipe__id', flat=True).distinct()
        )
        shopping_cart = RecipeIngredient.objects.filter(
            recipe__id__in=recipes_id
        )
        list = {}
        for ingredient in shopping_cart:
            if ingredient.ingredient.name in list.keys():
                list[f'{ingredient.ingredient.name}'] += ingredient.amount
            else:
                list[f'{ingredient.ingredient.name}'] = ingredient.amount
        with open(
            'api/carts/myshoppingcart.txt',
            'w+',
            encoding="utf-8"
        ) as f:
            for key, value in list.items():
                f.write('%s:%s\n' % (key, value))
            response = HttpResponse(f, content_type='text/plain')
            response['Content-Disposition'] = (
                'attachment; filename=myshoppingcart.txt'
            )
        return response
