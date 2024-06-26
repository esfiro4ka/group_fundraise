from django.core.cache import cache
from rest_framework import mixins, viewsets

from apps.collects.models import Collect
from config.settings import COLLECT_CACHE_KEY_PREFIX, COLLECTS_CACHE_KEY

from .models import Payment
from .serializers import PaymentSerializer
from .tasks import send_email_for_donor


class PaymentViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """Вьюсет для создания платежей.

    При создании платежа на групповой сбор донору отправляется уведомление
    об успешной операции.

    При создании платежа на групповой денежный сбор кэш с информацией
    о сборе и списке сборов удаляется.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_email = request.user.email
        amount = response.data['amount']
        collect_id = response.data['collect']
        collect = Collect.objects.get(id=collect_id)
        collect_title = collect.title
        send_email_for_donor.delay(user_email, amount, collect_title)
        if response.status_code == 201:
            cache.delete(COLLECTS_CACHE_KEY)
            collect_id = str(response.data['collect'])
            cache.delete(COLLECT_CACHE_KEY_PREFIX + collect_id)
        return response
