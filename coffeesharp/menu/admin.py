from django.contrib import admin
from django.contrib.admin import AdminSite
from django.core.checks import messages

from .models import Menu, Category

class CustomAdminSite(AdminSite):
    site_header = "Панель управления кофейней"
    site_title = "Кофейня Admin"
    index_title = "Добро пожаловать в админку кофейни"

    def each_context(self, request):
        context = super().each_context(request)
        context['css'] = 'admin/css/admin.css'
        return context

# заменим стандартную админку
custom_admin_site = CustomAdminSite(name='admin')



# Register your models here.
class HasCoverFilter(admin.SimpleListFilter):
    title = 'Наличие обложки'
    parameter_name = 'has_cover'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'С обложкой'),
            ('no', 'Без обложки'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(cover__isnull=False)
        if self.value() == 'no':
            return queryset.filter(cover__isnull=True)
        return queryset

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'cat','tags','is_published']
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'cat','time_create',  'is_published', 'brief_info','days_since_creation',)
    list_display_links = ('title',)
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    list_filter = ['cat__name', 'is_published',HasCoverFilter]
    actions = ['set_published','set_draft']
    search_fields = ['title__startswith', 'cat__name']
    filter_horizontal = ['tags']

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count =queryset.update(is_published=Menu.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Menu.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!",messages.WARNING )

    @admin.display(description="Краткое описание")
    def brief_info(self, menu: Menu):
        return f"Описание {len(menu.content)} символов."

    @admin.display(description="Свежесть новости")
    def days_since_creation(self, obj):
        from datetime import datetime, timezone
        return (datetime.now(timezone.utc) - obj.time_create).days

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

