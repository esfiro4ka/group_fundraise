from rest_framework import serializers

from .models import Collect
from apps.payments.serializers import PaymentForCollectSerializer


class CollectSerializer(serializers.ModelSerializer):
    collected_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        label='Собранная сумма'
    )
    donors_number = serializers.IntegerField(
        read_only=True,
        label='Количество дарителей'
    )
    collect_feed = PaymentForCollectSerializer(
        source='payments',
        many=True,
        read_only=True,
        label='Лента сбора'
    )

    class Meta:
        model = Collect
        fields = '__all__'
