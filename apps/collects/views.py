from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Count, Sum

from .models import Collect
from .serializers import CollectReadSerializer, CollectWriteSerializer


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CollectReadSerializer
        return CollectWriteSerializer

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            collected_amount=Sum('payments__amount'),
            donors_number=Count('payments__donor', distinct=True)
        )
        return queryset

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
