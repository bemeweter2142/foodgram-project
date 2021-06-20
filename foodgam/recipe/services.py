
import io

from django.conf import settings
from django.db.models import Count, Q, Sum
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .models import Recipe, RecipeIngredient, ShopList


def create_page(page):
    pdfmetrics.registerFont(TTFont(
        'FreeSans',
        str(settings.BASE_DIR) + r'\recipe\fonts\FreeSans.ttf'
        )
    )
    page.setFont('FreeSans', 14)
    page.drawString(180, 800, f'Список ингредиентов для покупки')
    page.setFont('FreeSans', 12)
    page.line(10, 780, 580, 780)
    return page


def create_pdf(request):
    step = 25
    top = 750
    bottom = 100
    left_padding = 70

    buffer = io.BytesIO()
    page = canvas.Canvas(buffer, pagesize=A4)
    page = create_page(page)

    ingredients = ShopList.objects.filter(user=request.user).select_related(
        'recipe'
    ).values(
        'recipe__ingredient__ingredient',
        'recipe__ingredient__measurement__measurement',
    ).annotate(amount=Sum('recipe__many_recipes__amount'))
    # количество линий на странице
    lines = 0
    # порядковый номер ингредиента
    number = 1
    for ingredient in ingredients:
        page.drawString(
            left_padding, top-lines*step,
            f'{number}. {ingredient["recipe__ingredient__ingredient"]} '
            f'({ingredient["recipe__ingredient__measurement__measurement"]}) -'
            f' {ingredient["amount"]} '
        )
        number += 1
        lines += 1

        # проверка на отсутствие места на странице
        if top-lines*step < bottom:
            lines = 0
            page.showPage()
            page = create_page(page)

    page.showPage()
    page.save()

    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='Список ингредиентов.pdf'
    )
