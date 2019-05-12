from django.conf import settings
from django.core.management.base import BaseCommand
from web3 import Web3

from main.models import AccountToTrack


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not settings.DEBUG:
            return
        provider = Web3.HTTPProvider('https://mainnet.infura.io/')
        w3 = Web3(provider)
        assert w3.isConnected(), "Can't connect to Infura"
        block_n = w3.eth.blockNumber - settings.CONFIRMATION_BLOCKS
        block = w3.eth.getBlock(block_n, full_transactions=True)

        for tx in block.transactions:
            account_id = tx['to']
            if account_id:
                AccountToTrack.objects.get_or_create(address=account_id)
