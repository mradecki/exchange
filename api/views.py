from api.models import ExchangeRate
from api.serializers import ExchangeRateSerializer
from django_filters import rest_framework as filters
from rest_framework import generics


class ExchangeRateHistoryView(generics.ListAPIView):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("currency",)
