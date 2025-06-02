from calendar import month
from datetime import datetime
import uuid

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from menu.forms import AddPostForm, UploadFileForm
from menu.models import Menu, Category, TagPost, UploadFiles, MenuGalleryCover
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.shortcuts import render

from menu.utils import DataMixin

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


def addcomment(request):
    return HttpResponse("Добавление статьи")


def feedback(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def category_coffee(request):
    return HttpResponse("Сорта кофе")


def category_drinks(request):
    return HttpResponse("Напитки")


def category_baking(request):
    return HttpResponse("Выпечка")


def category_breakfast(request):
    return HttpResponse("Завтраки")


def category_sandwich(request):
    return HttpResponse("Сэндвичи")


def category_desserts(request):
    return HttpResponse("Десерты")


class ShowPost(DataMixin,DetailView):
    model = Menu
    template_name = 'menu/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title=context['post'])

    def get_object(self, queryset=None):
        return get_object_or_404(Menu.published,slug=self.kwargs[self.slug_url_kwarg])


class MenuHome(DataMixin, ListView):
    def get_queryset(self):
        return Menu.published.all().select_related('cat')
    template_name = 'menu/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None,**kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs), title='Главная страница', cat_selected=0, )



def handle_uploaded_file(f):
     name = f.name
     ext = ''
     if '.' in name:
         ext = name[name.rindex('.'):]
         name = name[:name.rindex('.')]
     suffix = str(uuid.uuid4())
     with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'menu/about.html',
                  {'title': 'О сайте', 'menu1': menu1, 'form': form})

def menu(request):
    return render(request, 'menu/menu.html',
                  {'title': 'Меню', 'menu1': menu1})


class MenuCategory(DataMixin,ListView):
    template_name = 'menu/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,title='Категория - ' + cat.name,cat_selected = cat.id,)

    def get_queryset(self):
        return Menu.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


def menu_slug(request, categ_slug):
    if request.GET:
        print(request.GET)
    if request.POST:
        print(request.POST)
    if categ_slug == 'main':
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Категория меню </h1><p >slug:{categ_slug}</p>")


def special_month(request, date):
    current_date = datetime.now()
    if date['year'] > current_date.year or (date['year'] == current_date.year and date['month'] > current_date.month):
        return HttpResponse(f"<h1>На этот период акции еще не известны {date['month']:02d}-{date['year']}</h1>")
    return HttpResponse(f"<h1>Доступные акции на {date['month']:02d}-{date['year']}</h1>")


def special(request):
    current_date = datetime.now()
    current_month_year = {'month': current_date.month, 'year': current_date.year}
    url = reverse('special_month', kwargs={'date': current_month_year})
    return HttpResponseRedirect(url)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class TagPostList(DataMixin, ListView):
    template_name = 'menu/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,title='Тег: ' + tag.tag)
    def get_queryset(self):
        return  Menu.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

class AddPage(DataMixin,CreateView):
    form_class = AddPostForm
    title_page = 'Добавление статьи'
    template_name = 'menu/addpage.html'
    success_url = reverse_lazy('home')

class UpdatePage(DataMixin,UpdateView):
    model = Menu
    fields = ['title', 'content', 'photo','is_published', 'cat']
    template_name = 'menu/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'

class DeletePage(DataMixin,DeleteView):
    model = Menu
    template_name = 'menu/delete.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление статьи'











