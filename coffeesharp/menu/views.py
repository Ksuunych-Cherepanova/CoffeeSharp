from calendar import month
from datetime import datetime
from menu.models import Menu
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.shortcuts import render

menu1 = [{'title': "О сайте", 'url_name': 'about'},
 {'title': "Добавить отзыв", 'url_name':
'addcomment'},
{'title': "Акции", 'url_name':
'special'},
{'title': "Меню", 'url_name':
'menu'},
 {'title': "Обратная связь", 'url_name':
'feedback'},
 {'title': "Войти", 'url_name': 'login'}
]




cats_db = [
{'id': 1, 'name': 'Адреса'},
{'id': 2, 'name': 'Контакты'},
{'id': 3, 'name': 'Вакансии'},
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


def show_post(request, post_slug):
 post = get_object_or_404(Menu, slug=post_slug)
 data = {
 'title': post.title,
 'menu1': menu1,
 'post': post,
 'cat_selected': 1,
 }
 return render(request, 'menu/post.html',
context=data)


def index(request):
    posts = Menu.published.all()
    data = {
        'title': 'Главная страница',
        'menu1': menu1,
        'posts': posts,
    }
    return render(request, 'menu/index.html',
context=data)


def about(request):
 return render(request, 'menu/about.html',
{'title': 'О сайте', 'menu1': menu1})


def menu(request):
    return render(request, 'menu/menu.html',
                  {'title': 'Меню', 'menu1': menu1})

def show_category(request, cat_id):
 data = {
 'title': 'Отображение по рубрикам',
 'menu1': menu1,
 'posts': Menu.published.all(),
 'cat_selected': cat_id,
 }
 return render(request, 'women/index.html',
context=data)


def menu_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    if request.POST:
        print(request.POST)
    if cat_slug == 'main':
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Категория меню </h1><p >slug:{cat_slug}</p>")


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
