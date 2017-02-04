from app import db
import datetime as dt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.social_id)

