from app import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(128), index=True, unique=True)
    nickname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime)
    btc_address = db.relationship('BitcoinAddress', backref='owner', uselist=False)
    credits = db.Column(db.Integer, default=0, nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.social_id)

class BitcoinAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(35), index=True, unique=True)
    label = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    txns = db.relationship('BitcoinTransaction', backref='address', lazy='dynamic')

    def __repr__(self):
        return '<BitcoinAddress {}>'.format(self.address)

class BitcoinTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('bitcoin_address.id'))
    txn_hash = db.Column(db.String(64), index=True, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    block_height = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<BitcoinTxn {}/{}>'.format(self.amount, self.txn_hash)

