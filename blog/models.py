from django.db import models


from django.utils.text import slugify
from django.urls import reverse

class BlogPost(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    content = models.TextField(verbose_name='Содержание')
    preview_image = models.ImageField(
        verbose_name='Превью-изображение',
        upload_to='media/blog/previews/',
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=False
    )
    views_count = models.PositiveIntegerField(
        verbose_name='Просмотры',
        default=0
    )

    class Meta:
        verbose_name = 'Статья блога'
        verbose_name_plural = 'Статьи блога'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        # Автоматическое обновление счетчика при открытии поста
        if self.pk:
            self.views_count += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.pk,))
