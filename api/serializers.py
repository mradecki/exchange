from api.models import ExchangeRate
from django.db import models
from rest_framework import serializers


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = ["value", "date", "currency"]
