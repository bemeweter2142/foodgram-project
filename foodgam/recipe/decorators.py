from django.core.exceptions import PermissionDenied


def author_or_admin(function):
    def check_author(request, *args, **kwargs):
        if (
            request.user.recipes.filter(id=kwargs['id']).exists()
            or request.user.is_superuser
        ):
            return function(request, *args, **kwargs)
        raise PermissionDenied()
    return check_author
