from rest_framework import serializers

from . import models


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountToTrack
        fields = ('address',)


class TransactionETHSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TransactionETH
        fields = '__all__'
