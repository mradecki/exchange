from urllib.error import HTTPError

import feedparser
from api.models import ExchangeRate
from celery import group, shared_task
from django.conf import settings


@shared_task()
def update_rates():

    tasks = []

    for currency in ExchangeRate.Currency.values:
        tasks.append(update_rate.s(currency=currency))

    group(tasks).apply_async(queue="api")


@shared_task(autoretry_for=(HTTPError,), retry_backoff=True)
def update_rate(currency):

    url = settings.URL_TEMPLATE.format(currency=currency)
    data = feedparser.parse(url)

    for entry in data.entries:

        value = entry["cb_exchangerate"].split("\n")[0]
        date = entry["updated"]

        ExchangeRate.objects.get_or_create(currency=currency, value=value, date=date)
