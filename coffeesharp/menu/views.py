from calendar import month
from datetime import datetime
import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from menu.forms import AddPostForm, UploadFileForm, CommentForm
from menu.models import Menu, Category, TagPost, UploadFiles, MenuGalleryCover, Reaction, Comment
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


class ShowPost(DataMixin, DetailView):
    model = Menu
    template_name = 'menu/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        context['comment_form'] = CommentForm()
        context['comments'] = post.comments.all()
        context['likes'] = post.reactions.filter(reaction='like').count()
        context['dislikes'] = post.reactions.filter(reaction='dislike').count()

        user_reaction = None
        if self.request.user.is_authenticated:
            user_reaction = post.reactions.filter(user=self.request.user).first()
        context['user_reaction'] = user_reaction.reaction if user_reaction else None

        return self.get_mixin_context(context, title=post)

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        if "comment_submit" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
        elif "reaction" in request.POST and request.user.is_authenticated:
            reaction_type = request.POST.get("reaction")
            Reaction.objects.update_or_create(
                post=post, user=request.user,
                defaults={"reaction": reaction_type}
            )

        return HttpResponseRedirect(reverse('post', kwargs={'post_slug': post.slug}))

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

@login_required(login_url='/admin/')
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

class AddPage(PermissionRequiredMixin, DataMixin,CreateView):
    form_class = AddPostForm
    title_page = 'Добавление статьи'
    template_name = 'menu/addpage.html'
    success_url = reverse_lazy('home')
    permission_required = 'menu.add_menu'
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

class UpdatePage(PermissionRequiredMixin,UpdateView):
    model = Menu
    fields = ['title', 'content', 'photo','is_published', 'cat']
    template_name = 'menu/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'menu.change_menu'

class DeletePage(DataMixin,DeleteView):
    model = Menu
    template_name = 'menu/delete.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление статьи'



@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author and not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Комментарий обновлен.")
            return redirect(comment.post.get_absolute_url())
    else:
        form = CommentForm(instance=comment)

    return render(request, 'menu/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author and not request.user.is_staff:
        return redirect('home')

    post_url = comment.post.get_absolute_url()
    comment.delete()
    messages.success(request, "Комментарий удален.")
    return redirect(post_url)








