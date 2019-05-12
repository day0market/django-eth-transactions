import logging
from decimal import Decimal

import redis
from django.conf import settings
from web3 import Web3

from .models import AccountToTrack, TransactionETH


def update_transactions():
    accounts = AccountToTrack.objects.all()
    if accounts.count() == 0:
        return

    provider = Web3.HTTPProvider('https://mainnet.infura.io/')
    w3 = Web3(provider)
    assert w3.isConnected(), "Can't connect to Infura"

    redis_ = redis.StrictRedis(host=settings.REDIS_HOST, port=6379)
    last_checked_block = redis_.get("last_checked_block")
    if last_checked_block:
        last_checked_block = int(last_checked_block.decode())
    block_to_check = w3.eth.blockNumber - settings.CONFIRMATION_BLOCKS

    if last_checked_block == block_to_check:
        return
    elif last_checked_block and last_checked_block > block_to_check:
        logging.error(f"Last checked block is probably wrong. It can't be before block to check"
                      f"Last checked: {last_checked_block}, Block to check: {block_to_check}")

    accounts_set = {a.address for a in accounts}
    if not last_checked_block:
        last_checked_block = block_to_check

    new_transactions = []
    for block_n in range(last_checked_block, block_to_check + 1):
        block = w3.eth.getBlock(block_n, full_transactions=True)
        found = get_block_transactions_for_accounts(block, accounts_set)
        if found:
            new_transactions.extend(found)

    redis_.set("last_checked_block", block_to_check)

    if new_transactions:
        for t in new_transactions:
            t.save()
        logging.info(f"Found and saved {len(new_transactions)} transactions")


def get_block_transactions_for_accounts(block, accounts_set):
    transactions = []
    for tx in block.transactions:
        transaction_accounts = {tx['to'], tx['from']}
        if transaction_accounts & accounts_set:
            timestamp = int(block.timestamp)
            transaction = TransactionETH.objects.get_or_create(
                block=block.number,
                transaction_hash=str(tx['hash'].hex()),
                fromAddress=tx['from'],
                toAddress=tx['to'],
                quantity=Decimal(tx['value']),
                input=tx['input'],
                timestamp=timestamp
            )

            # transactions.append(transaction)
            continue

    return transactions
