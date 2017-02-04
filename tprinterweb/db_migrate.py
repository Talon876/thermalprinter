#!/usr/bin/env python
# -*- coding: utf-8 -*-
import imp
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
"""After updating the database models, run this script to generate the upgrade script and apply it"""

# Get current version of the repository with the given connection string under version control of the migrate repo
version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

# Generate new migration script based on migration repo's models
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (version + 1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, 'wt').write(script)

# Upgrade database to latest version in the repistory and print the version number
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as {}'.format(migration))
print('Current version: {}'.format(str(v)))


