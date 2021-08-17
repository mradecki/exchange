from django.db import models


class ExchangeRate(models.Model):
    class Currency(models.TextChoices):

        AUD = "aud"
        BGN = "bgn"
        BRL = "brl"
        CAD = "cad"
        CHF = "chf"
        CNY = "cny"
        CZK = "czk"
        DKK = "dkk"
        EEK = "eek"
        GBP = "gbp"
        HKD = "hkd"
        HRK = "hrk"
        HUF = "huf"
        IDR = "idr"
        INR = "inr"
        ISK = "isk"
        JPY = "jpy"
        KRW = "krw"
        MXN = "mxn"
        MYR = "myr"
        NOK = "nok"
        NZD = "nzd"
        PHP = "php"
        PLN = "pln"
        RON = "ron"
        RUB = "rub"
        SEK = "sek"
        SGD = "sgd"
        THB = "thb"
        TRY = "try"
        USD = "usd"
        ZAR = "zar"

    currency = models.CharField(max_length=3, choices=Currency.choices)
    value = models.DecimalField(max_digits=12, decimal_places=5)
    date = models.DateTimeField()

    class Meta:
        ordering = ["currency", "date"]
