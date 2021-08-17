import unittest
from datetime import datetime
from unittest.mock import Mock, call, patch
from urllib.error import HTTPError

from api.models import ExchangeRate
from api.tasks import update_rate, update_rates
from api.utils import ExchangeRateFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import itertools as it


class TestExchangeRate(APITestCase):
    def test_list_endpoint_should_return_list_of_exchange_rates_sorted_by_currency_and_date(
        self,
    ):

        # GIVEN
        rates = ExchangeRateFactory.create_batch(size=50)

        # WHEN
        response = self.client.get(reverse("rate-list"), format="json")

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        currencies = [r["currency"] for r in results]
        self.assertEqual(currencies, sorted(currencies))
        for currency, g in it.groupby(results, key=lambda r: r["currency"]):
            dates = [entry["date"] for entry in g]
            self.assertEqual(sorted(dates), dates)

    def test_list_endpoint_should_support_filtering_by_currency(self):

        # GIVEN
        ExchangeRateFactory.create(currency=ExchangeRate.Currency.AUD)
        ExchangeRateFactory.create_batch(size=50)

        # WHEN
        response = self.client.get(
            reverse("rate-list") + f"?currency={ExchangeRate.Currency.AUD}",
            format="json",
        )

        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        currencies = [r["currency"] for r in results]
        self.assertTrue(all(c == ExchangeRate.Currency.AUD for c in currencies))

    def test_supported_currencies(self):

        self.assertEqual(
            set(
                [
                    "aud",
                    "bgn",
                    "brl",
                    "cad",
                    "chf",
                    "cny",
                    "czk",
                    "dkk",
                    "eek",
                    "gbp",
                    "hkd",
                    "hrk",
                    "huf",
                    "idr",
                    "inr",
                    "isk",
                    "jpy",
                    "krw",
                    "mxn",
                    "myr",
                    "nok",
                    "nzd",
                    "php",
                    "pln",
                    "ron",
                    "rub",
                    "sek",
                    "sgd",
                    "thb",
                    "try",
                    "usd",
                    "zar",
                ]
            ),
            set(ExchangeRate.Currency.values),
        )


class TestTasks(unittest.TestCase):
    @patch("api.tasks.feedparser")
    @patch("api.models.ExchangeRate.objects.get_or_create")
    def test_update_rate_task_should_create_entities(self, get_or_create, feedparser):

        # GIVEN
        currency = ExchangeRate.Currency.values[0]
        value1, value2 = "111.111", "222.222"
        date1, date2 = datetime.now().isoformat(), datetime.now().isoformat()

        feedparser.parse.return_value = Mock(
            entries=[
                {
                    "cb_exchangerate": value1,
                    "updated": date1,
                },
                {
                    "cb_exchangerate": value2,
                    "updated": date2,
                },
            ]
        )

        # WHEN
        update_rate(currency)

        # THEN
        get_or_create.assert_has_calls(
            [
                call(currency=currency, value=value1, date=date1),
                call(currency=currency, value=value2, date=date2),
            ]
        )

    @patch("api.tasks.group")
    def test_update_rates_task(self, group):

        # WHEN
        update_rates()

        # THEN
        group.assert_called_once_with(
            [update_rate.s(currency=c) for c in ExchangeRate.Currency.values]
        )
