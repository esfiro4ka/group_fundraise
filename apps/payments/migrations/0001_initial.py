# Generated by Django 5.0.2 on 2024-02-26 20:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Bank Cards', 'Банковские карты'), ('Instant Payment System', 'Система быстрых платежей'), ('Yandex Pay', 'Yandex Pay')], default='Bank Cards', max_length=50, verbose_name='Тип платежа')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма платежа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время и дата платежа')),
                ('collect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='collects.collect', verbose_name='Денежный сбор')),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Даритель')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
                'ordering': ('id',),
            },
        ),
    ]
