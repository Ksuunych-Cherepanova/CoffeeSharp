from calendar import month
from datetime import datetime

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
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


data_db = [
 {'id': 1, 'title': 'Новинки в меню: авторский раф "Карамельное облако"!', 'content':
'Друзья, у нас отличная новость для всех любителей нежных, сливочных напитков! Встречайте нашу новую звезду – раф "Карамельное облако"! 🌤️☕ Этот восхитительный кофе подарит вам настоящее наслаждение благодаря сочетанию мягкого сливочного вкуса, карамельной сладости и легкого ванильного аромата. Его бархатистая текстура окутывает уютом, создавая ощущение тепла и комфорта. "Карамельное облако" идеально подойдет для неспешных утренних минут или приятных вечеров в кругу друзей. Попробуйте этот шедевр и дайте себе возможность окунуться в мир сладкого наслаждения с первого глотка! 💛✨', 'is_published': True},
 {'id': 2, 'title': 'Акция "Вторая чашка в подарок"!', 'content':
'С 12 по 18 марта закажите любой напиток и получите вторую чашку бесплатно – для друга, любимого человека или просто для себя! 💕☕ Проводите весну с теплом и вкусом в нашей кофейне!', 'is_published': True},
 {'id': 3, 'title': 'Десерт месяца – "Шоколадная фантазия"!', 'content':
'Встречайте эксклюзивный десерт марта – "Шоколадная фантазия"! Это сочетание насыщенного шоколадного мусса, хрустящего миндального слоя и воздушного крема. Пробуйте и делитесь впечатлениями! 🍫✨', 'is_published': True},
{'id': 4, 'title': 'Живая музыка по пятницам!', 'content':
'Каждую пятницу в 19:00 у нас выступают талантливые музыканты! Живые звуки гитары, уютная атмосфера и аромат свежесваренного кофе – идеальный рецепт для хорошего вечера. Приходите за вдохновением! 🎸☕💫', 'is_published': True},

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


def show_post(request, post_id):
 return HttpResponse(f"Отображение статьи с id ={post_id}")


def index(request):
 data = {
 'title': 'CoffeeSharp',
 'menu1': menu1,
 'posts': data_db,
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
    return HttpResponse(f"<h1>категория</h1>")


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
