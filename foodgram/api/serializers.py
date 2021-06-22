
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipe.models import Favorite, Follow, Ingredient, Measurement, ShopList


class CustomModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return self.Meta.model.objects.create(**validated_data)


class PurchasesSerializer(CustomModelSerializer):
    class Meta:
        fields = ('recipe', )
        model = ShopList


class FavoriteSerializer(CustomModelSerializer):
    class Meta:
        fields = ('recipe', )
        model = Favorite


class FollowSerializer(CustomModelSerializer):
    class Meta:
        fields = ('author', )
        model = Follow

    def validate_author(self, data):
        user = self.context['request'].user
        if user.id == data:
            raise ValidationError('Подписка на самого себя недопустима!')
        return data


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('measurement', )


class IngredientSerializer(serializers.ModelSerializer):
    measurement = MeasurementSerializer(many=False)

    class Meta:
        model = Ingredient
        fields = ('ingredient', 'measurement', )
