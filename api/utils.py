import datetime

import factory
import factory.fuzzy
from api import models
from django.utils.timezone import get_default_timezone


class ExchangeRateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ExchangeRate

    currency = factory.fuzzy.FuzzyChoice(models.ExchangeRate.Currency.values)
    value = factory.fuzzy.FuzzyDecimal(1, 100, 3)
    date = factory.fuzzy.FuzzyDateTime(start_dt=datetime.datetime(2021, 1, 1, tzinfo=get_default_timezone()))
