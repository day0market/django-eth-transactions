import logging

import redis
from django.conf import settings
from django.test import TestCase
from web3 import Web3

from main.models import AccountToTrack, TransactionETH
from main.transactions_updater import update_transactions


class RedisTest(TestCase):

    def test_redis(self):
        redis_ = redis.StrictRedis(host=settings.REDIS_HOST, port=6379)
        redis_.set("test_value", 15)
        value = redis_.get("test_value")
        print(value)
        int_value = int(value.decode())
        self.assertEqual(15, int_value)


class TransactionUpdaterTestCase(TestCase):

    def setUp(self):
        provider = Web3.HTTPProvider('https://mainnet.infura.io/')
        w3 = Web3(provider)
        assert w3.isConnected(), "Can't connect to Infura"
        fromBlock = w3.eth.blockNumber - settings.CONFIRMATION_BLOCKS - 3
        toBlock = w3.eth.blockNumber - settings.CONFIRMATION_BLOCKS + 2
        for i in range(fromBlock, toBlock):
            block = w3.eth.getBlock(i, full_transactions=True)
            for tx in block.transactions:
                account_id = tx['to']
                if account_id:
                    account, created = AccountToTrack.objects.get_or_create(address=account_id)
                    if not created:
                        continue
                    account.save()
        logging.info("Accounts created")

    def test_update_transactions(self):
        redis_ = redis.StrictRedis(host=settings.REDIS_HOST, port=6379)
        redis_.delete("last_checked_block")

        provider = Web3.HTTPProvider('https://mainnet.infura.io/')
        w3 = Web3(provider)

        block_n = w3.eth.blockNumber - settings.CONFIRMATION_BLOCKS
        update_transactions()
        transactions = TransactionETH.objects.all()

        for s in transactions:
            self.assertEqual(block_n, s.block)

        self.assertTrue(transactions.count() > 0)
        last_checked_block = redis_.get("last_checked_block")
        if last_checked_block:
            last_checked_block = int(last_checked_block.decode())

        self.assertEqual(last_checked_block, block_n)
