from django.db.models import Count

from menu.models import Category, TagPost
from django import template

from menu.views import menu1

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('menu/list_tags.html')
def show_all_tags():
    return {"tags":TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
@register.simple_tag
def get_menu():
 return menu1