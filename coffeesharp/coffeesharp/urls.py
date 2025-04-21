
from menu import views

from django.contrib import admin
from django.urls import path, include

from menu.views import page_not_found
admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Кофейня CoffeeSharp"

handler404 = page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('menu.urls')),

]