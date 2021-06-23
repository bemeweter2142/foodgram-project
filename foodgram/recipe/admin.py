from django.contrib import admin

from .models import (Favorite, Ingredient, Measurement, 
                     Recipe, RecipeIngredient, Tag)


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


class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('measurement',)
    search_fields = ('measurement',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'color',)
    search_fields = ('tag',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Tag, TagAdmin)
