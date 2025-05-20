from calendar import month
from datetime import datetime
import uuid
from menu.forms import AddPostForm, UploadFileForm
from menu.models import Menu, Category, TagPost, UploadFiles, MenuGalleryCover
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.shortcuts import render

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
        'cat_selected': 0,
    }
    return render(request, 'menu/index.html',
                  context=data)


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


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Menu.published.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu1': menu1,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'menu/index.html', context=data)


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


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Menu.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu1': menu1,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'menu/index.html', context=data)


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('home')
            except Exception as e:
                form.add_error(None, f'Ошибка добавления поста: {e}')
        else:
            form.add_error(None, 'Форма невалидна')
    else:
        form = AddPostForm()

    return render(request, 'menu/addpage.html',
                  {'menu1': menu1, 'title': 'Добавление статьи', 'form': form})

