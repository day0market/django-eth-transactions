from django.db import models


class AccountToTrack(models.Model):
    address = models.CharField(max_length=155, unique=True)

    def __str__(self):
        return f"{self.address}"


class TransactionETH(models.Model):
    block = models.BigIntegerField()
    transaction_hash = models.CharField(max_length=500, unique=True)
    fromAddress = models.CharField(max_length=125)
    toAddress = models.CharField(max_length=125)
    quantity = models.DecimalField(decimal_places=0, max_digits=1000)
    input = models.CharField(max_length=10000000)
    timestamp = models.BigIntegerField()

    def __str__(self):
        return f"{self.transaction_hash} from {self.fromAddress} to {self.toAddress}"
