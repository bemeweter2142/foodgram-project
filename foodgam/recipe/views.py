from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import author_or_admin
from .forms import RecipeForm
from .models import (Follow, Recipe, RecipeIngredient,
                     ShopList, Tag, User)
from .services import create_pdf


@login_required
def download_list(request):
    pdf = create_pdf(request)
    ShopList.objects.filter(user=request.user).delete()
    return pdf


@login_required
def new_recipe(request):
    if request.method != 'POST':
        form = RecipeForm()
        return render(request, 'formRecipe.html', {'form': form})

    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'formRecipe.html', {'form': form})

    form.save(commit=False, author=request.user)
    return redirect('index')


@login_required
@author_or_admin
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    form = RecipeForm(
        request.POST or None,
        request.FILES or None,
        instance=recipe
    )

    if not form.is_valid():
        return render(
            request,
            'formRecipe.html',
            {'form': form, 'recipe': recipe, }
        )
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    recipe = form.save(commit=False, author=recipe.author)
    return redirect('single_recipe', id=recipe.id,)


@login_required
@author_or_admin
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.user.is_superuser or request.user == recipe.author:
        recipe.delete()
    return redirect('index')


def index(request):
    all_tags, tags = get_tags(request)
    recipes = Recipe.objects.filter(
        tag__tag__in=tags
    ).select_related(
        'author'
    ).distinct()

    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    title = 'Рецепты'
    header = 'Рецепты'
    return render(
        request,
        'index.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
            'title': title,
            'header': header,
        }
    )


@login_required
def favorite(request):
    all_tags, tags = get_tags(request)
    recipes = Recipe.objects.prefetch_related().filter(
        tag__tag__in=tags,
        recipe__user=request.user,
    ).select_related(
        'author'
    ).distinct()

    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    title = 'Избранное'
    header = 'Избранное'
    return render(
        request,
        'index.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
            'title': title,
            'header': header,
        }
    )


def author_recipe(request, username):
    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author__username=username)
    tags = Tag.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'authorRecipe.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'author': author
        })


@login_required
def my_follow(request):
    authors = Follow.objects.select_related('author').filter(
        user=request.user
    ).prefetch_related('author')
    tags = Tag.objects.all()
    paginator = Paginator(authors, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'myFollow.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
        })


def get_tags(request):
    all_tags = Tag.objects.all()
    tags = request.GET.getlist('tag', [tag.tag for tag in all_tags])
    return all_tags, tags


@login_required
def shop_list(request):
    recipes = ShopList.objects.select_related('recipe').filter(
        user=request.user
    )
    return render(request, 'shopList.html', {'recipes': recipes})


def single_page(request, id):
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related('ingredient'), id=id
    )
    return render(request, 'singlePage.html', {'recipe': recipe})
