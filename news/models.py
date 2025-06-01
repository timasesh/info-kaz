from django.db import models
from django.utils.text import slugify
from django.db.models import Max

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL-слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug_exists = True
            counter = 1
            while slug_exists:
                slug = base_slug
                if counter > 1:
                    slug = f'{base_slug}-{counter}'
                if not Category.objects.filter(slug=slug).exists():
                    self.slug = slug
                    slug_exists = False
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст новости')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    image = models.ImageField(upload_to='news_images/', verbose_name='Изображение', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news', verbose_name='Категория')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name='URL-слаг')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            # Если slugify вернул пустую строку, используем значение по умолчанию
            if not base_slug:
                 base_slug = 'article'

            slug = base_slug
            counter = 1
            # Проверяем уникальность среди объектов News, исключая текущий объект (для обновлений)
            # Используем loop для поиска уникального слага
            while News.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Contact(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В обработке'),
        ('completed', 'Завершено'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    admin_response = models.TextField(verbose_name='Ответ администратора', blank=True, null=True)
    response_date = models.DateTimeField(verbose_name='Дата ответа', blank=True, null=True)

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}" 