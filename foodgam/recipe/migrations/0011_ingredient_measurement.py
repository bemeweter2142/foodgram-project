# Generated by Django 3.2.3 on 2021-05-31 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0010_remove_ingredient_measurement'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='measurement',
            field=models.CharField(default=None, max_length=100, verbose_name='Единицы измерений'),
        ),
    ]
