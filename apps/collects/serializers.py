from rest_framework import serializers

from apps.payments.serializers import PaymentForCollectSerializer

from .models import Collect


class CollectReadSerializer(serializers.ModelSerializer):
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


class CollectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = ('title',
                  'reason',
                  'description',
                  'planned_amount',
                  'cover_image',
                  'finished_at')
