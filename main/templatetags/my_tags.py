from django import template

register = template.Library()


@register.filter()
def mymedia(data):
    if data:
        return f'/media/{data}'
    return '/media/no_image.png'
