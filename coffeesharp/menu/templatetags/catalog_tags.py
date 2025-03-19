from django import template

register = template.Library()

@register.inclusion_tag('menu/includes/menu_categoryes.html')
def show_categories():
    menu_items = [
        {"name": "Кофе", "url": "category_coffee"},
        {"name": "Напитки", "url": "category_drinks"},
        {"name": "Выпечка", "url": "category_baking"},
        {"name": "Десерты", "url": "category_desserts"},
        {"name": "Завтраки", "url": "category_breakfast"},
        {"name": "Сендвичи", "url": "category_sandwich"},

    ]
    return {"menu_items": menu_items}
