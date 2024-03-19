from django.contrib.auth.models import User
from django.db import models


class Reason(models.TextChoices):
    """Варианты повода для сбора."""

    BIRTHDAY = ('Birthday', 'День рождения')
    WEDDING = ('Wedding', 'Свадьба')
    OTHER = ('Other', 'Другое')


class Collect(models.Model):
    """Модель группового денежного сбора."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор сбора'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    reason = models.CharField(
        max_length=20,
        choices=Reason,
        default=Reason.OTHER,
        verbose_name='Повод'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    planned_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Запланированная сумма'
    )
    cover_image = models.ImageField(
        upload_to='collect_covers/',
        null=True,
        blank=True,
        verbose_name='Обложка сбора'
    )
    finished_at = models.DateTimeField(
        verbose_name='Дата и время завершения сбора'
    )

    class Meta:
        verbose_name = 'Групповой денежный сбор'
        verbose_name_plural = 'Групповые денежные сборы'
        ordering = ('id',)

    def __str__(self):
        return self.title
