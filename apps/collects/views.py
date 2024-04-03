from django.core.cache import cache
from django.db.models import Count, Sum
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from config.settings import COLLECT_CACHE_KEY_PREFIX, COLLECTS_CACHE_KEY

from .models import Collect
from .permissions import CollectPermission
from .serializers import CollectReadSerializer, CollectWriteSerializer
from .tasks import send_email_for_collect_author


class CollectViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для просмотра, создания, обновления и удаления информации о
    групповых денежных сборах.

    При создании группового денежного сбора автору отправляется уведомление
    об успешной операции.

    При просмотре группового сбора или списка групповых сборов информация
    берется из кэша. Если данные в кэше отстуствуют, информация берется из
    базы данных и полученный ответ сохраняется в кэше для будущих запросов.

    При создании группового сбора из кэша удаляется информация о списке
    групповых сборов. При обновлении и удалении группового сбора из кэша
    удаляется как информация о данном групповом сборе, так и о списке
    групповых сборов.
    """

    queryset = Collect.objects.all()
    permission_classes = [CollectPermission]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CollectReadSerializer
        return CollectWriteSerializer

    def list(self, request, *args, **kwargs):
        cached = cache.get(COLLECTS_CACHE_KEY)
        if cached:
            return cached
        response = super().list(request, *args, **kwargs)
        response.add_post_render_callback(
            lambda r: cache.set(COLLECTS_CACHE_KEY, r)
        )
        return response

    def retrieve(self, request, *args, **kwargs):
        collect_id = kwargs['pk']
        cache_key = COLLECT_CACHE_KEY_PREFIX + collect_id
        cached = cache.get(cache_key)
        if cached:
            return cached
        response = super().retrieve(request, *args, **kwargs)
        response.add_post_render_callback(
            lambda r: cache.set(cache_key, r)
        )
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_email = request.user.email
        collect_title = request.data['title']
        send_email_for_collect_author.delay(user_email, collect_title)
        if response.status_code == 201:
            cache.delete(COLLECTS_CACHE_KEY)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            cache.delete(COLLECTS_CACHE_KEY)
            collect_id = kwargs['pk']
            cache.delete(COLLECT_CACHE_KEY_PREFIX + collect_id)
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            cache.delete(COLLECTS_CACHE_KEY)
            collect_id = kwargs['pk']
            cache.delete(COLLECT_CACHE_KEY_PREFIX + collect_id)
        return response

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            collected_amount=Sum('payments__amount'),
            donors_number=Count('payments__donor', distinct=True)
        )
        return queryset

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
