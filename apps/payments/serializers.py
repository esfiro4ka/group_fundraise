from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей."""

    class Meta:
        model = Payment
        fields = ('collect', 'type', 'amount')


class DonorForCollectSerializer(serializers.ModelSerializer):
    """Сериализатор для доноров, отправивших платежи
    на групповой денежный сбор.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class PaymentForCollectSerializer(serializers.ModelSerializer):
    """Сериализатор для ленты платежей группового денежного сбора."""

    donor = DonorForCollectSerializer()

    class Meta:
        model = Payment
        fields = ('donor', 'amount', 'created_at')
