from django.db import models
from django.contrib.auth.models import User
from apps.collects.models import Collect


class Type(models.TextChoices):
    """Варианты типа платежа."""

    BANK_CARDS = ('Bank Cards', 'Банковские карты')
    IPS = ('Instant Payment System', 'Система быстрых платежей')
    YANDEX_PAY = ('Yandex Pay', 'Yandex Pay')


class Payment(models.Model):
    """Модель платежа."""

    collect = models.ForeignKey(
        Collect,
        related_name='payments',
        on_delete=models.CASCADE,
        verbose_name='Денежный сбор'
    )
    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Даритель'
    )
    type = models.CharField(
        max_length=50,
        choices=Type,
        default=Type.BANK_CARDS,
        verbose_name='Тип платежа'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма платежа'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время и дата платежа'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('id',)

    def __str__(self):
        return f'{self.donor.username} - {self.amount}'
