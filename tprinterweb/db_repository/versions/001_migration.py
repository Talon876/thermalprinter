from sqlalchemy import *
from migrate import *
import datetime

from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('social_id', String(length=128)),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('created_at', DateTime, default=ColumnDefault(datetime.datetime.utcnow)),
    Column('last_login', DateTime),
    Column('last_seen', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['last_login'].create()
    post_meta.tables['user'].columns['last_seen'].create()
    post_meta.tables['user'].columns['nickname'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['last_login'].drop()
    post_meta.tables['user'].columns['last_seen'].drop()
    post_meta.tables['user'].columns['nickname'].drop()
