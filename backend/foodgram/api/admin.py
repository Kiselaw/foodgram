from django.contrib import admin

from api.models import (Cart, Favorite, Follow, Ingredient, Recipe,
                        RecipeIngredient, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'author', 'text', 'cooking_time',)
    list_display = (
        'id', 'name',
        'author', 'text',
        'cooking_time', 'image',
        'favorite_count',
    )
    list_editable = ('name', 'author', 'text', 'cooking_time', 'image',)
    list_filter = ('name', 'author', 'cooking_time', 'tags',)
    inlines = (RecipeIngredientInline,)
    read_only_fields = ('favorite_count',)

    def favorite_count(self, instance):
        return instance.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'slug', 'color',)
    list_editable = ('name', 'slug', 'color',)
    list_filter = ('name', 'slug', 'color',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'measurement_unit')
    list_editable = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    search_fields = ('user', 'author',)
    list_display = ('id', 'user', 'author',)
    list_filter = ('user', 'author',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('id', 'user', 'recipe',)
    list_filter = ('user', 'recipe',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('id', 'user', 'recipe',)
    list_filter = ('user', 'recipe',)
