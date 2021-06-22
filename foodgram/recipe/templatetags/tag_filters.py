from django import template

register = template.Library()


@register.filter(name='parse_tags')
def parse_tags(get):
    return get.getlist('tag')


@register.filter(name='set_tag_qs')
def set_tag_qs(request, tag):
    new_req = request.GET.copy()
    tags = new_req.getlist('tag')
    if tag.tag in tags:
        tags.remove(tag.tag)
    else:
        tags.append(tag.tag)
    new_req.setlist('tag', tags)
    return new_req.urlencode()
