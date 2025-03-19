
from menu import views

from django.contrib import admin
from django.urls import path, include

from menu.views import page_not_found

handler404 = page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('menu.urls')),
    path('about/',include('menu.urls')),
    path('post/',include('menu.urls')),
    path('menu/',include('menu.urls')),
    path('addcomment/',include('menu.urls')),
    path('special/',include('menu.urls')),
    path('category/',include('menu.urls')),
]