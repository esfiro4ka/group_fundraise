from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserForCollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class PaymentForCollectSerializer(serializers.ModelSerializer):
    donor = UserForCollectSerializer()

    class Meta:
        model = Payment
        fields = ('donor', 'amount', 'created_at')
