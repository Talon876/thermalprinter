from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import basedir, USD_TO_CREDIT_RATIO
from tprinterbot import celeryapp
from tprinterbot import actions as printeractions

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

def wrap_celery(flaskapp, celapp):
    TaskBase = celapp.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with flaskapp.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celapp.Task = ContextTask
    return celapp

app = Flask(__name__)
app.config.from_object('config')

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@app.context_processor
def inject_debug():
    return {'debug': app.debug}

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/tprinter.log', 'a', 10 * 1024 * 1024, 20)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('tprinter initializing')

    app.wsgi_app = ReverseProxied(app.wsgi_app)

db = SQLAlchemy(app)

celeryapp = wrap_celery(app, celeryapp)
celeryapp.conf.task_routes = {
    'app.tasks.*': {
        'queue': 'app'
    }
}

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import bitcoin
blockchain = bitcoin.BlockchainInfo(
        app.config['BITCOIN']['wallet']['guid'],
        app.config['BITCOIN']['wallet']['password'],
        app.config['BITCOIN']['service'])

def convert_btc_to_credits(btc_amount):
    btc_to_usd = blockchain.exchange_rate('USD')
    usd = btc_amount * btc_to_usd
    credits = usd * USD_TO_CREDIT_RATIO
    app.logger.info('Converting {} btc to {} USD is {} credits'.format(btc_to_usd, usd, credits))
    return credits

from app import views, models, tasks

