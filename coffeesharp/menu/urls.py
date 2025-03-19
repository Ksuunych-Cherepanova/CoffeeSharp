from django.urls import path, re_path, register_converter
from menu import views, converters
register_converter(converters.MonthYearConverter, "monthyear")

urlpatterns = [
    path('', views.index, name = 'home'),
    path('about/', views.about, name='about'),
    path('menu/<slug:cat_slug>/', views.menu_slug, name = 'menu_category'),
    path('menu/', views.menu, name = 'menu'),
    path('<int:post_id>/', views.show_post,name='post'),
    path('addcomment/', views.addcomment, name='addcomment'),
    path('feedback/', views.feedback, name='feedback'),
    path('login/', views.login, name='login'),
    path('special/', views.special, name = 'special'),
    path('special/<monthyear:date>/', views.special_month, name = 'special_month'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
    path('coffee/', views.category_coffee, name='category_coffee'),
    path('drinks/', views.category_drinks, name='category_drinks'),
    path('baking/', views.category_baking, name='category_baking'),
    path('desserts/', views.category_desserts, name='category_desserts'),
    path('breakfast/', views.category_breakfast, name='category_breakfast'),
    path('sandwich/', views.category_sandwich, name='category_sandwich'),



]

