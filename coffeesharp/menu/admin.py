from django.contrib import admin
from django.contrib.admin import AdminSite
from django.core.checks import messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .forms import AddPostForm
from .models import Menu, Category,MenuGalleryCover

class MenuGalleryCoverInline(admin.StackedInline):
    model = MenuGalleryCover
    extra = 0
    max_num = 1
    can_delete = True
    verbose_name = "Обложка поста"
    verbose_name_plural = "Обложка поста"

    readonly_fields = ['cover_preview']

    def cover_preview(self, obj):
        if obj.image:
            return format_html(f"<img src='{obj.image.url}' width='100'>")
        return "Нет изображения"

    cover_preview.short_description = "Превью"

class CustomAdminSite(AdminSite):
    site_header = "Панель управления кофейней"
    site_title = "Кофейня Admin"
    index_title = "Добро пожаловать в админку кофейни"

    def each_context(self, request):
        context = super().each_context(request)
        context['css'] = 'admin/css/admin.css'
        return context

custom_admin_site = CustomAdminSite(name='admin')




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
    save_on_top = True
    form = AddPostForm
    fields = ['title', 'slug', 'content','cover_preview', 'photo','cat','tags','is_published']
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['cover_preview','post_photo']
    list_display = ('title','cover_preview','post_photo', 'cat','time_create',  'is_published','days_since_creation',)
    list_display_links = ('title',)
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    list_filter = ['cat__name', 'is_published',HasCoverFilter]
    actions = ['set_published','set_draft']
    search_fields = ['title__startswith', 'cat__name']
    filter_horizontal = ['tags']
    inlines = [MenuGalleryCoverInline]

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count =queryset.update(is_published=Menu.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Menu.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!",messages.WARNING )

    @admin.display(description="Изображение")
    def post_photo(self, menu: Menu):
        if menu.photo:
            return mark_safe(f"<img src='{menu.photo.url}'width=50>")
        return "Без фото"

    @admin.display(description="Обложка")
    def cover_preview(self, obj):
        if hasattr(obj, 'cover') and obj.cover.image:
            return mark_safe(f"<img src='{obj.cover.image.url}' width=50>")
        return "Без обложки"

    @admin.display(description="Свежесть новости")
    def days_since_creation(self, obj):
        from datetime import datetime, timezone
        return (datetime.now(timezone.utc) - obj.time_create).days

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

