from app import app
from app import celeryapp
from app.models import BitcoinTransaction
from celery.schedules import crontab

@celeryapp.task
def bitcoin_info():
    txn_count = BitcoinTransaction.query.filter_by(credit_txn=None).count()
    msg = 'Found {} unprocessed transactions'.format(txn_count)
    app.logger.info(msg)
    return txn_count

@celeryapp.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, bitcoin_info.s(), name='find unprocessed bitcoin transactions')

