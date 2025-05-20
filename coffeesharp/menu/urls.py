from django.urls import path, re_path, register_converter
from menu import views, converters
register_converter(converters.MonthYearConverter, "monthyear")
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'home'),
    path('about/', views.about, name='about'),
    path('menu/<slug:categ_slug>/', views.menu_slug, name = 'menu_category'),
    path('menu/', views.menu, name = 'menu'),
    path('addcomment/', views.addcomment, name='addcomment'),
    path('feedback/', views.feedback, name='feedback'),
    path('login/', views.login, name='login'),
    path('special/', views.special, name = 'special'),
    path('special/<monthyear:date>/', views.special_month, name = 'special_month'),
    path('coffee/', views.category_coffee, name='category_coffee'),
    path('drinks/', views.category_drinks, name='category_drinks'),
    path('baking/', views.category_baking, name='category_baking'),
    path('desserts/', views.category_desserts, name='category_desserts'),
    path('breakfast/', views.category_breakfast, name='category_breakfast'),
    path('sandwich/', views.category_sandwich, name='category_sandwich'),
    path('post/<slug:post_slug>/', views.show_post,name='post'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('addpage/', views.addpage, name='addpage'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
