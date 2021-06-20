from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import Favorite, Ingredient, Recipe, RecipeIngredient


# Регистрация в Админке возможности добавления ингредиентов в рецепте
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


# Добавление модуля в раздел Рецептов
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('title', 'author', 'get_tags', 'get_count_favorite',)
    list_filter = ('tag',)
    search_fields = ('title', 'tag__tag', 'author__username',)

    # функция вывода всех тэгов для рецепта в админке
    def get_tags(self, obj):
        return '; '.join([p.tag for p in obj.tag.all()])

    # функция подсчета добавления рецепта в избранное
    def get_count_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    # Переименовать стандартное имя функций в админке
    get_tags.short_description = 'Тэги'
    get_count_favorite.short_description = 'Добавлено в избранное'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'measurement')
    search_fields = ('ingredient',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)

# Регистрация в Админке всех остальных моделей, пока разработка идет
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
