import json
import random
import string
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from main.models import AccountToTrack, TransactionETH


class TestAPI(TestCase):
    def setUp(self):
        self._client = APIClient()

    @staticmethod
    def gen_random_string(self, length=15):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def test_account_api_add(self):
        normal_account = 'some_test_account1'
        response = self._client.post(
            "/api/accounts/",
            json.dumps({'address': normal_account}),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)

        added_acc = AccountToTrack.objects.get(address=normal_account)
        self.assertEqual(added_acc.address, normal_account)

        # Case when we trying to add account that's already exists

        response = self._client.post(
            "/api/accounts/",
            json.dumps({'account_id': normal_account}),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

        # Case when we trying to add empty account

        empty_account = ""
        response = self._client.post(
            "/api/accounts/",
            json.dumps({'account_id': normal_account}),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

        self.assertRaises(AccountToTrack.DoesNotExist,
                          lambda: AccountToTrack.objects.get(address=empty_account))

    def test_transactions_api_fetch(self):
        transactions = [
            TransactionETH(
                block=200,
                transaction_hash=self.gen_random_string(15),
                fromAddress=self.gen_random_string(10),
                toAddress=self.gen_random_string(10),
                quantity=Decimal(random.randint(0, 150_000_000)),
                input=self.gen_random_string(25),
                timestamp=timezone.datetime(2012, 1, 1, 14, 20).timestamp()
            ),

            TransactionETH(
                block=45488,
                transaction_hash=self.gen_random_string(15),
                fromAddress=self.gen_random_string(10),
                toAddress=self.gen_random_string(10),
                quantity=Decimal(random.randint(0, 150_000_000)),
                input=self.gen_random_string(25),
                timestamp=timezone.datetime(2012, 1, 1, 14, 20).timestamp()
            ),

            TransactionETH(
                block=8889,
                transaction_hash=self.gen_random_string(15),
                fromAddress=self.gen_random_string(10),
                toAddress=self.gen_random_string(10),
                quantity=Decimal(random.randint(0, 150_000_000)),
                input=self.gen_random_string(25),
                timestamp=timezone.datetime(2019, 1, 1, 14, 20).timestamp()
            ),

            TransactionETH(
                block=855,
                transaction_hash=self.gen_random_string(15),
                fromAddress=self.gen_random_string(10),
                toAddress=self.gen_random_string(10),
                quantity=Decimal(random.randint(0, 150_000_000)),
                input=self.gen_random_string(25),
                timestamp=timezone.datetime(2014, 1, 1, 14, 20).timestamp()
            ),

            TransactionETH(
                block=454,
                transaction_hash=self.gen_random_string(15),
                fromAddress=self.gen_random_string(10),
                toAddress=self.gen_random_string(10),
                quantity=Decimal(random.randint(0, 150_000_000)),
                input=self.gen_random_string(25),
                timestamp=timezone.datetime(2015, 1, 1, 14, 20).timestamp()
            ),

            TransactionETH(
                block=500,
                transaction_hash=self.gen_random_string(15),
                fromAddress=self.gen_random_string(10),
                toAddress=self.gen_random_string(10),
                quantity=Decimal(random.randint(0, 150_000_000)),
                input=self.gen_random_string(25),
                timestamp=timezone.datetime(2015, 2, 1, 14, 20).timestamp()
            )
        ]

        for t in transactions:
            t.save()

        response = self._client.get("/api/transactions/?format=json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(transactions), len(response.data['results']))

        response = self._client.get("/api/transactions/?format=json&fromDate=2013-01-01")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 4)

        response = self._client.get("/api/transactions/?format=json&fromDate=2013-01-01&toDate=2016-01-01")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)

        response = self._client.get(
            f"/api/transactions/?format=json&fromDate=2013-01-01&fromAddress={transactions[2].fromAddress}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

        response = self._client.get(
            f"/api/transactions/?format=json&fromDate=2013-01-01&toAddress={transactions[1].toAddress}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)
