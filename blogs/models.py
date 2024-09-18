from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.CharField(max_length=150, verbose_name='slug')
    body = models.TextField(**NULLABLE, verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blogs/', **NULLABLE, verbose_name='Превью')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

        permissions = [('can_published', 'Can published blog')]
