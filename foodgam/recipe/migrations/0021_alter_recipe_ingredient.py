# Generated by Django 3.2.3 on 2021-06-13 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0020_alter_recipe_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(blank=True, null=True, related_name='ingredients', through='recipe.RecipeIngredient', to='recipe.Ingredient', verbose_name='Ингредиенты'),
        ),
    ]
