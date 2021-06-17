from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from recipe.models import Favorite, Follow, Ingredient

from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, PurchasesSerializer)


class MixinAndViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):

    def get_object(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg],
            **kwargs,
        }

        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(user=self.request.user)
        success = instance.delete()
        return Response({'success': bool(success)}, status=HTTP_200_OK)


class PurchasesViewSet(ListModelMixin, MixinAndViewSet):
    serializer_class = PurchasesSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'recipe'

    def get_queryset(self):
        return self.request.user.users_shop.all()


class FavoriteViewSet(MixinAndViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'recipe'


class FollowViewSet(MixinAndViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'author'


class IngredientViewSet(ListModelMixin, GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('ingredient',)
