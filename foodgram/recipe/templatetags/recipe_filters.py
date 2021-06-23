from django import template
from django.contrib.auth import get_user_model

from ..models import Favorite, Follow, ShopList

register = template.Library()
User = get_user_model()


@register.filter
def is_following(user, author):
    try:
        return Follow.objects.filter(user=user, author=author).exists()
    except AttributeError:
        return False


@register.filter
def is_favorite(recipe, user):
    try:
        return Favorite.objects.filter(user=user, recipe=recipe).exists()
    except AttributeError:
        return False


@register.filter
def is_in_shop_list(recipe, user):
    try:
        return ShopList.objects.filter(user=user, recipe=recipe).exists()
    except AttributeError:
        return False
