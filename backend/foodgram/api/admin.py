from django.contrib import admin

from api.models import (Cart, Favorite, Follow, Ingredient, Recipe,
                        RecipeIngredient, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'author', 'text', 'cooking_time',)
    list_display = (
        'id', 'name',
        'author', 'text',
        'cooking_time', 'image',
        'favorite_count', 'link'
    )
    list_editable = ('name', 'author', 'text', 'cooking_time', 'image',)
    list_filter = ('name', 'author', 'cooking_time', 'tags',)
    list_display_links = ('link',)
    inlines = (RecipeIngredientInline,)
    read_only_fields = ('favorite_count',)

    def favorite_count(self, instance):
        return instance.favorites.count()


class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'slug', 'color', 'link',)
    list_editable = ('name', 'slug', 'color',)
    list_filter = ('name', 'slug', 'color',)
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ('link',)


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'link',)
    list_editable = ('name',)
    list_filter = ('name',)
    list_display_links = ('link',)


class FollowAdmin(admin.ModelAdmin):
    search_fields = ('user', 'author',)
    list_display = ('user', 'author', 'link',)
    list_filter = ('user', 'author',)
    list_display_links = ('link',)


class FavoriteAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('id', 'user', 'recipe', 'link',)
    list_filter = ('user', 'recipe',)
    list_display_links = ('link',)


class CartAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('id', 'user', 'recipe', 'link',)
    list_filter = ('user', 'recipe',)
    list_display_links = ('link',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
