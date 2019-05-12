from celery import task

from .transactions_updater import update_transactions


@task()
def update_transactions_worker():
    update_transactions()
