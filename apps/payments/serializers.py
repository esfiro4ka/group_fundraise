from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Payment


class PaymentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('collect', 'type', 'amount')


class DonorForCollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class PaymentForCollectSerializer(serializers.ModelSerializer):
    donor = DonorForCollectSerializer()

    class Meta:
        model = Payment
        fields = ('donor', 'amount', 'created_at')
