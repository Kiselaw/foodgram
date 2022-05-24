import base64
import uuid

import webcolors
from django.core.files.base import ContentFile
from rest_framework import serializers

from users.models import CustomUser
from users.serializers import CustomUserSerializer

from .models import (Cart, Favorite, Follow, Ingredient, Recipe,
                     RecipeIngredient, Tag)


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени!')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            extension = format.split('/')[-1]
            id = uuid.uuid4()
            data = ContentFile(
                base64.b64decode(imgstr), name=str(id)[:10] + '.' + extension
            )
        return data


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'amount', 'measurement_unit')
        model = RecipeIngredient

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipePostSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True
    )

    class Meta:
        fields = (
            'id', 'name',
            'image', 'text',
            'ingredients', 'tags',
            'cooking_time',
        )
        model = Recipe

    def create(self, validated_data):
        validated_data.pop('recipeingredient_set')
        ingredients = self.initial_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        tags_id = []
        for tag in tags_data:
            tags_id.append(tag.id)
        tags = Tag.objects.filter(pk__in=tags_id)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            amount = ingredient['amount']
            id = ingredient['id']
            recipe_ingredient = Ingredient.objects.get(pk=id)
            RecipeIngredient.objects.create(
                amount=amount,
                recipe=recipe,
                ingredient=recipe_ingredient)
        recipe.save()
        return recipe


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set', read_only=True, many=True
    )
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name',
            'author', 'image',
            'text', 'ingredients',
            'tags', 'cooking_time',
            'is_favorited', 'is_in_shopping_cart',
        )
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user.favorites.filter(recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user.in_cart.filter(recipe=obj).exists()
        return False

    def to_representation(self, instance):
        response = super(RecipeSerializer, self).to_representation(instance)
        response['image'] = instance.image.url
        return response


class FollowsSerializer(CustomUserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'is_subscribed',
            'recipes', 'recipes_count',
        )
        model = CustomUser

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit'
        )
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        serializer = FollowsRecipesSerializer(recipes, many=True)
        return serializer.data


class FollowsRecipesSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        fields = (
            'id', 'name',
            'image', 'cooking_time',
        )
        model = Recipe


class FollowPostSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    # Умнее пока не придумал

    class Meta:
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'is_subscribed',
            'recipes', 'recipes_count',
        )
        model = Follow

    def validate(self, data):
        author_id = self.context.get('view').kwargs.get('author_id')
        author = CustomUser.objects.get(pk=author_id)
        user = self.context['request'].user
        if Follow.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны!'
            )
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data

    def get_id(self, obj):
        return obj.author.id

    def get_email(self, obj):
        return obj.author.email

    def get_first_name(self, obj):
        return obj.author.first_name

    def get_last_name(self, obj):
        return obj.author.last_name

    def get_username(self, obj):
        return obj.author.username

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return user.following.filter(author=obj.author).exists()

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    def get_recipes(self, obj):
        recipes = obj.author.recipes.all()
        serializer = FollowsRecipesSerializer(recipes, many=True)
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time',)
        model = Favorite

    def validate(self, data):
        recipe_id = self.context.get('view').kwargs.get('recipe_id')
        recipe = Recipe.objects.get(pk=recipe_id)
        user = self.context['request'].user
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Уже добавлено в избранное!')
        return data

    def get_id(self, obj):
        return obj.recipe.id

    def get_name(self, obj):
        return obj.recipe.name

    def get_image(self, obj):
        image_url = obj.recipe.image.url
        return image_url

    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time


class CartSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time',)
        model = Cart

    def validate(self, data):
        recipe_id = self.context.get('view').kwargs.get('recipe_id')
        recipe = Recipe.objects.get(pk=recipe_id)
        user = self.context['request'].user
        if Cart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Уже добавлено в список покупок!')
        return data

    def get_id(self, obj):
        return obj.recipe.id

    def get_name(self, obj):
        return obj.recipe.name

    def get_image(self, obj):
        image_url = obj.recipe.image.url
        return image_url

    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time
