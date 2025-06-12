from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Menu, Category, MenuGalleryCover, Comment
from django.core.validators import MinLengthValidator,MaxLengthValidator
from .models import Menu, Category, TagPost
from django_select2.forms import Select2MultipleWidget

@deconstructible
class RussianValidator:
    ALLOWED_CHARS ="АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'
    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."
    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})

class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")


class AddPostForm(forms.ModelForm):
    cover_image = forms.ImageField(label="Обложка для новости", required=False)

    # Валидация длины заголовка
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина заголовка не должна превышать 50 символов.')
        return title

    # Валидация для изображения (ограничим размер файла)
    def clean_cover_image(self):
        cover_image = self.cleaned_data.get('cover_image')
        if cover_image:
            if cover_image.size > 5 * 1024 * 1024:  # Ограничение на 5MB
                raise ValidationError("Размер изображения не должен превышать 5MB.")
        return cover_image

    # Категория
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Выберите категорию",
        label="Категория",
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    # Теги
    tags = forms.ModelMultipleChoiceField(
        queryset=TagPost.objects.all(),
        widget=Select2MultipleWidget(attrs={'class': 'form-tag-input'}),
        required=False,
        label="Теги"
    )

    class Meta:
        model = Menu
        fields = ['title', 'slug', 'content','cover_image', 'photo',  'is_published', 'cat', 'tags']
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }

    def save(self, commit=True):
        menu = super().save(commit=False)

        if commit:
            menu.save()

            image = self.cleaned_data.get('cover_image')
            if image:
                # Удалим старую обложку, если она уже была (по желанию)
                MenuGalleryCover.objects.filter(menu=menu).delete()
                MenuGalleryCover.objects.create(menu=menu, image=image)

        return menu

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Оставьте комментарий...'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите ваш комментарий...'})
        }


