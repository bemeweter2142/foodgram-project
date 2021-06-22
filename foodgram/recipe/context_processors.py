def shop_list_count(request):
    try:
        count = request.user.users_shop.count()
    except AttributeError:
        count = 0
    return {
        'shop_list_count': int(count)
    }
