# Встроенная модель для работы с пользователям
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


# Если есть, выводятся ФИ, иначе логин
def get_user_name(self):
    if self.first_name or self.last_name:
        return f'{self.first_name} {self.last_name}'
    return self.username


# Определение модели пользователя
User = get_user_model()


User.add_to_class('__str__', get_user_name)


# Сначала описываются базовые модели, а затем модели с ForeinKey
class Measurement(models.Model):
    measurement = models.CharField(
        max_length=30,
        verbose_name='Единицы измерений',
    )

    class Meta:
        ordering = ['measurement']
        verbose_name = 'Единица измерений'
        verbose_name_plural = 'Единицы измерений'

    def __str__(self):
        return self.measurement


class Ingredient(models.Model):
    ingredient = models.CharField(
        max_length=100,
        verbose_name='Название ингредиента',
    )
    measurement = models.ForeignKey(
        Measurement,
        on_delete=models.CASCADE,
        verbose_name='Единицы измерений',
        default=None,
        related_name='measurements',
    )

    class Meta:
        ordering = ['ingredient']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.ingredient}'


class Tag(models.Model):
    tag = models.CharField(
        max_length=30,
        verbose_name='Название Тэга',
    )
    color = models.CharField(
        max_length=15,
        verbose_name='Цвет',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['tag']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.tag


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    # Может быть несколько ингредиентов у рецепта
    ingredient = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
    )
    # Может быть несколько тэгов у рецепта
    tag = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Тэги',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Например, Борщ по-русски'
    )
    description = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Например, почему Вам нравится этот рецепт?'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение рецепта',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1)],
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.title}, автор рецепта: {self.author.username}'


# Модель связывает Рецепт, Ингредиенты, Единицы измерений и количество
class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='many_ingredients',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        default=None,
        related_name='many_recipes',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
        default=10,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Рецепты-Ингредиенты'
        verbose_name_plural = 'Рецепты-Ингредиенты'

    def __str__(self):
        return (f'{self.ingredient} - {self.amount}'
                f' {self.ingredient.measurement}')


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан на',
    )

    # Проверка на существование подписки
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow')
            ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'


# отдельная модель добавления в избранное. Можно было добавить поле в саму
# модель Recipe, как many-to-many, но мне так показалось лучше.
class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Избранный рецепт',
    )

    # Проверка на добавление в избранное
    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.user.username} добавил в избранное {self.recipe.title}'


# модель списков покупок
class ShopList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users_shop',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shops',
        verbose_name='Рецепт в списке покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        # Проверка на добавление в список
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shop')
        ]

    def __str__(self):
        return f'{self.user.username} добавил в список {self.recipe.title}'
