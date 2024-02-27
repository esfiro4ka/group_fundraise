from rest_framework import viewsets

from .models import Payment
from .serializers import PaymentReadSerializer, PaymentWriteSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PaymentReadSerializer
        return PaymentWriteSerializer
