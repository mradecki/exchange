from django.db import models


class ExchangeRate(models.Model):
    class Currency(models.TextChoices):

        USD = "usd"
        JPY = "jpy"
        BGN = "bgn"
        CZK = "czk"
        DKK = "dkk"
        EEK = "eek"
        GBP = "gbp"
        HUF = "huf"
        PLN = "pln"
        RON = "ron"
        SEK = "sek"
        CHF = "chf"
        ISK = "isk"
        NOK = "nok"
        HRK = "hrk"
        RUB = "rub"
        TRY = "try"
        AUD = "aud"
        BRL = "brl"
        CAD = "cad"
        CNY = "cny"
        HKD = "hkd"
        IDR = "idr"
        INR = "inr"
        KRW = "krw"
        MXN = "mxn"
        MYR = "myr"
        NZD = "nzd"
        PHP = "php"
        SGD = "sgd"
        THB = "thb"
        ZAR = "zar"

    currency = models.CharField(max_length=3, choices=Currency.choices)
    value = models.DecimalField(max_digits=12, decimal_places=5)
    date = models.DateTimeField()

    class Meta:
        ordering = ["currency", "date"]
