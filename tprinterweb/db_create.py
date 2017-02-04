#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
"""Use this script to create the initial database repository and database"""

# Uses sqlalchemy to create all models
db.create_all()

if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    # Create migration repository
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database-repo')
    # Mark database as under this repository's version control
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    # Marks database as under this repository's version control using the latest version from the migration repo
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

