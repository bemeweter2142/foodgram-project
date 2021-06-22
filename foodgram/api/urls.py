from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('purchases', views.PurchasesViewSet, basename='purchases')
router.register('favorites', views.FavoriteViewSet, basename='favorites')
router.register('subscriptions', views.FollowViewSet, basename='subscriptions')
router.register('ingredients', views.IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),

]
