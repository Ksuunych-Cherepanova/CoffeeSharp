menu1 = [{'title': "О сайте", 'url_name': 'about'},
         {'title': "Добавить пост", 'url_name':
             'addpage'},
         {'title': "Акции", 'url_name':
             'special'},
         {'title': "Меню", 'url_name':
             'menu'},
         {'title': "Обратная связь", 'url_name':
             'feedback'},
         {'title': "Войти", 'url_name': 'login'}
         ]
class DataMixin:
    title_page = None
    extra_context = {}
    paginate_by = 3

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] =self.title_page
        if 'menu1' not in self.extra_context:
            self.extra_context['menu1'] = menu1

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page
        context['menu1'] = menu1
        context['cat_selected'] = None
        context.update(kwargs)
        return context
