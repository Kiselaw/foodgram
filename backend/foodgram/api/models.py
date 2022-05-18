from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(max_length=150)
    measurement_unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True)
    color = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, null=False)
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        null=False
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1, 'Добавьте количество')],
        null=False
    )


class Recipe(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='recipes', null=False
    )
    name = models.CharField(max_length=200, null=False)
    image = models.ImageField(upload_to='recipes/', null=False)
    text = models.TextField(blank=False, null=False)
    cooking_time = models.IntegerField(
        blank=False, validators=[MinValueValidator(1, 'Добавьте время')]
    )
    ingredients = models.ManyToManyField(Ingredient, through=RecipeIngredient)
    tags = models.ManyToManyField(
        Tag, related_name='recipes')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevention_of_self_following',
            ),
        ]

    def __str__(self):
        return f'user: {self.user}, author: {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            ),
        ]

    def __str__(self):
        return f'user: {self.user}, recipe: {self.recipe}'


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='in_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_cart'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_cart',
            ),
        ]

    def __str__(self):
        return f'user: {self.user}, recipe: {self.recipe}'
