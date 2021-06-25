from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .models import Ingredient, Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    # вводятся названия ингредиентов, а не их ключи, поэтому новая переменная
    ingredients = forms.CharField(
        required=False,
        label='Ингредиенты'
    )
    cooking_time = forms.IntegerField(
        label='Время приготовления',
        min_value=1,
        validators=[MinValueValidator(1)]
    )
    class Meta:
        model = Recipe
        fields = [
            'title',
            'tag',
            'ingredients',
            'cooking_time',
            'description',
            'image',
        ]

    # clean для поля ingredients
    def clean_ingredients(self):
        ingredients = []
        # поиск по ключам, которые передаются в POST запросе
        for key in self.data.keys():
            # в JS ингредиент через input вводится как Ingredient
            if key.startswith('Ingredient'):
                title = self.data[key]
                # в JS кол-во через input вводится как valueIngredient
                amount = int(self.data['value'+key])
                if amount < 1:
                    raise ValidationError(
                        f'Указано неверное количество ингредиента "{title}"'
                    )
                else:
                    ingredients.append({
                        'title': title,
                        'amount': amount,
                        }
                    )
                if ingredients.count(ingredients[-1]) > 1:
                    raise ValidationError(
                        f'Ингредиент {title} дублируется!')
        if len(ingredients) == 0:
            raise ValidationError('Ингредиенты отсутствуют')
        return ingredients

    def clean_cooking_time(self):
        cooking_time = int(self.data['cooking_time'])
        if cooking_time < 1:
            raise ValidationError(
                f'Время должно быть больше 1 мин.')
        return cooking_time

    def save(self, author, commit=True):
        recipe = super().save(commit=False)
        recipe.author = author
        recipe.save()

        ingredients = self.cleaned_data['ingredients']
        self.cleaned_data['ingredients'] = []
        self.save_m2m()

        for item in ingredients:
            ingredient_name = item['title']
            amount = item['amount']
            ingredient = Ingredient.objects.get(ingredient=ingredient_name)
            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )
            recipe_ingredient.save()
        return recipe
