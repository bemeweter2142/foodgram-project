from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('me/favorite/', views.favorite, name='favorite'),
    path('recipe/<int:id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('new/', views.new_recipe, name='new'),
    path('me/follow/', views.my_follow, name='follow'),
    path('me/shop_list/', views.shop_list, name='shop_list'),
    path('recipe/<int:id>/', views.single_page, name='single_recipe'),
    path('recipe/<int:id>/delete', views.delete_recipe, name='delete_recipe'),
    path('download/', views.download_list, name='shoplist_download'),
    path('<str:username>/', views.author_recipe, name='author_recipe')
]
