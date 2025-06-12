from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.core.validators import MinLengthValidator,MaxLengthValidator

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Menu.Status.PUBLISHED)


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д':
        'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и':
             'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п':
             'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х':
             'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y',
         'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}
    return "".join(map(lambda x: d[x] if d.get(x,
                                               False) else x, s.lower()))


class Menu(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255 ,verbose_name="Заголовок")
    slug = models.SlugField(max_length=255,
                            db_index=True, unique=True, validators=[MinLengthValidator(5),MaxLengthValidator(100),])

    content = models.TextField(blank=True ,verbose_name="Текст поста")
    time_create = models.DateTimeField(auto_now_add=True ,verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True ,verbose_name="Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x:  (bool(x[0]), x[1]), Status.choices)),
                        default=Status.DRAFT, verbose_name="Статус")

    cat = models.ForeignKey('Category' ,on_delete=models.CASCADE, related_name='posts' ,verbose_name="Категория")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags' ,verbose_name="Теги")
    days_count = models.PositiveIntegerField(blank=True ,default=0)

    objects = models.Manager()
    published = PublishedManager()

    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",
                              default=None, blank=True, null=True,
                              verbose_name="Фото")
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.SET_NULL, related_name='posts',
                               null=True, default=None)

    class Meta:
        verbose_name = 'Новости кофейни'
        verbose_name_plural = 'Новости кофейни'
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100,
                           db_index=True)
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    def get_absolute_url(self):

        return reverse('tag', kwargs={'tag_slug':
                                          self.slug})

    def __str__(self):

        return self.tag


class Category(models.Model):
        name = models.CharField(max_length=100,
                                db_index=True ,verbose_name="Категория")
        slug = models.SlugField(max_length=255,
                                unique=True, db_index=True)

        def get_absolute_url(self):
            return reverse('category', kwargs={'cat_slug': self.slug})

        def __str__(self):
            return self.name

        class Meta:
            verbose_name = 'Категория'
            verbose_name_plural = 'Категории'


class MenuGalleryCover(models.Model):
    menu = models.OneToOneField(Menu ,on_delete=models.SET_NULL, null=True, blank=True, related_name='cover')
    image = models.ImageField(upload_to='menu/news_covers/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Обложка для: {self.menu.title}"

class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')

class Comment(models.Model):
    post = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    content = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post}'

class Reaction(models.Model):
    class ReactionType(models.TextChoices):
        LIKE = 'like', 'Лайк'
        DISLIKE = 'dislike', 'Дизлайк'

    post = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=ReactionType.choices)

    class Meta:
        unique_together = ('post', 'user')