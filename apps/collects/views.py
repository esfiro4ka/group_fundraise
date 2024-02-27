from rest_framework import viewsets
from django.db.models import Count, Sum


from .models import Collect
from .serializers import CollectSerializer


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            collected_amount=Sum('payments__amount'),
            donors_number=Count('payments__donor', distinct=True)
        )
        return queryset
