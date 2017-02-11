import os
basedir = os.path.abspath(os.path.dirname(__file__))

TEMPLATES_AUTO_RELOAD = True

TASK_QUEUE_URI=os.environ.get('TASK_QUEUE_URI', '')
TPRINTER_DB=os.environ.get('TPRINTER_DB', os.path.join(basedir, 'tprint.db'))

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(basedir, 'tprint.db'))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('CSRF_SECRET',
        'decd571c33fa7184ce8c4fb3732d26c6f0745193cf1408274c38067fe51e68d0fdc9aef535f5a99fda4e8573b875521e')

OAUTH_CREDENTIALS = {
    'twitch': {
        'client_id': os.environ.get('TWITCH_CLIENT_ID', ''),
        'client_secret': os.environ.get('TWITCH_CLIENT_SECRET', ''),
    }
}

BITCOIN = {
    'wallet': {
        'guid': os.environ.get('WALLET_GUID', ''),
        'password': os.environ.get('WALLET_PASS', ''),
    },
    'service': os.environ.get('WALLET_SERVICE', 'http://localhost:3000')
}

PORT = int(os.environ.get('PORT', 9001))
SERVER_NAME=os.environ.get('SERVER_NAME', None)

USD_TO_CREDIT_RATIO = 15000

