from rest_framework import mixins, viewsets
from django.core.cache import cache

from config.settings import COLLECTS_CACHE_KEY, COLLECT_CACHE_KEY_PREFIX
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            cache.delete(COLLECTS_CACHE_KEY)
            collect_id = str(response.data['collect'])
            cache.delete(COLLECT_CACHE_KEY_PREFIX + collect_id)
        return response
