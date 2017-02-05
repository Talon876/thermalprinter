from sqlalchemy import *
from migrate import *
import datetime

from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
bitcoin_address = Table('bitcoin_address', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('address', String(length=35)),
    Column('label', String(length=64)),
    Column('user_id', Integer),
)

bitcoin_transaction = Table('bitcoin_transaction', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('address_id', Integer),
    Column('txn_hash', String(length=64), nullable=False),
    Column('amount', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('block_height', Integer, nullable=False),
    Column('credit_txn_id', Integer),
)

credit_transaction = Table('credit_transaction', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('credit_amount', Integer, nullable=False),
    Column('is_debit', Boolean, nullable=False, default=ColumnDefault(True)),
    Column('pending', Boolean, nullable=False, default=ColumnDefault(True)),
    Column('timestamp', DateTime, default=ColumnDefault(datetime.datetime.utcnow)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('social_id', String(length=128)),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('created_at', DateTime, default=ColumnDefault(datetime.datetime.utcnow)),
    Column('last_login', DateTime),
    Column('last_seen', DateTime),
    Column('credits', Integer, nullable=False, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['bitcoin_address'].create()
    post_meta.tables['bitcoin_transaction'].create()
    post_meta.tables['credit_transaction'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['bitcoin_address'].drop()
    post_meta.tables['bitcoin_transaction'].drop()
    post_meta.tables['credit_transaction'].drop()
    post_meta.tables['user'].drop()
